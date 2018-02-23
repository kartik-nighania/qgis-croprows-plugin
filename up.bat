set /P comment=Enter Comment: 
git add . 
git commit -m "%comment%"
git push origin master --force