echo "Starting remotes:"
git remote -v
echo "Adding remotes"
git remote set-url origin --add --push https://github.com/tallandcollege/project-3-scrum-pokermon.git
git remote set-url origin --add --push https://github.com/JortVlaming/project-3-pokermon.git
echo "Remotes added"
git remote -v
echo "Should have 2 remotes with (push) at the end"