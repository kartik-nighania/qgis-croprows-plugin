@echo off
set /P comment=Enter Comment: 
git add . 
git commit -m "%comment%"
git push origin master --force
rem https://github.com/AndresHerrera/qgis-croprows-plugin.git