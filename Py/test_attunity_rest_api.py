import json
import datetime
import requests
import base64
import urllib3
import copy


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
api_base_url = 'https://34.106.63.146/attunityenterprisemanager/api/v1/'

auth_str = "{}:{}".format("ATTUNITY-DEV\\daniel_vasilan", "FM9_AeJKt/q@jtJ")
print(auth_str)
auth_enc = base64.b64encode(auth_str.encode('utf-8'))
print(auth_enc)

l_headers = {"Authorization": "Basic " + auth_enc.decode('utf-8')}
s = requests.Session()
r = s.get(url=api_base_url + 'login', headers=l_headers, verify=False)
if r.status_code == 200:
    session_id = r.headers.get('EnterpriseManager.APISessionID')
    resp_headers = r.headers

    l_tsk_headers = {'EnterpriseManager.APISessionID': session_id}
    r_task = s.get(url="{}servers/{}/tasks/{}?action=export".format(api_base_url, 'Local Server', 'test-add-cols'),
                   headers=l_tsk_headers, verify=False)

    if r_task.status_code == 200:
        task_json = json.loads(r_task.text)

        new_task = copy.deepcopy(task_json['cmd.replication_definition']['tasks'][0])
        new_task['task']['name'] = 'test-task-duplicated'
        task_json['cmd.replication_definition']['tasks'] = [new_task]
        task_json['name'] = 'test-task-duplicated__2020-12-18--13-40-17-203725'

        task_str_new = str(task_json)
        duplicate_headers = {'EnterpriseManager.APISessionID': session_id,
                             'Content-Length': str(len(task_str_new))
                             }
        dupl_req = requests.Request('POST',
                                    url="{}servers/{}?action=import".format(api_base_url, 'Local Server'),
                                    #url="{}servers/{}/tasks/{}?action=import".format(api_base_url, 'Local Server',
                                    #                                        'test-add-cols-duplicate'),
                                    data=task_str_new,
                                    headers=duplicate_headers
                                    )
        dupl_prep = dupl_req.prepare()
        dupl_prep.body = task_str_new
        r_task_duplicate = s.send(dupl_prep, verify=False)

    print(session_id)
else:
    print('[Error] on login' + str(r.content))
