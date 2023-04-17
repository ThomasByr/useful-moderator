#!/usr/bin/env bash
# -*- coding: utf-8 -*-

processes=$(pgrep -u "$USER" -f "useful-moderator.py")
xargs kill -9 <<< "$processes" > /dev/null 2>&1
printf "\033[97mkilled processes:\033[0m\n%s\n\n" "$processes"

python3 useful-moderator.py > bot.log 2>&1 &
