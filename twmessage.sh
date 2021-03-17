#!/bin/bash
message=$(notmuch show "$(notmuch search id:$(task _get $1.messageid|tr -d "<>")|awk '{ print $1 }'|cut -d: -f2)")
partid=$(echo "$message"|grep -i "text/plain"|cut -d: -f2|cut -d, -f1)
notmuch show --part $partid $(notmuch search id:$(task _get $1.messageid|tr -d "<>")|awk '{ print $1 }'|cut -d: -f2)
