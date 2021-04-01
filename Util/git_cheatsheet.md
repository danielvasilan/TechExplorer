

git pull origin master

git checkout -b my-local-branch

git commit -a -m "This is a summary of the changes that I made in this commit."


# check the latest 15 commits
git log --oneline head -15



# if your work is not completed you can do the rebase
# when you execute this command your commit(s) will be placed on top of the commits from the master branch, 
#   and their ids will change each time you perform a rebase
git pull origin master --rebase



# If your work is complete you can perform an interactive rebase in order to squash your commits into one commit
git checkout master

git pull origin master

git checkout my-branch

git rebase -i master

# The commands above update your local master 
# However, if you are not interested in updating your local master branch 
#   You can just execute this command in order to perform the interactive rebase

git pull origin master --rebase=interactive
