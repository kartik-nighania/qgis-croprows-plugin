#!/bin/bash
echo -n "Enter Comment:"
read comment 
git add . 
git commit -m "$comment"
git push origin master --force
#https://github.com/AndresHerrera/qgis-croprows-plugin.git