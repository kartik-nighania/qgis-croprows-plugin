#!/bin/sh
read -p 'Enter Comment' comment 
git add . 
git commit -m $comment
git push origin master --force