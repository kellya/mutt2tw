#!/usr/bin/env python
import notmuch
import sys
import html2text
from taskw import TaskWarrior

try:
    taskno = sys.argv[1]
except IndexError:
    print("You must specify a task number")
    sys.exit()
w = TaskWarrior(marshal=True)
try:
    messageid = w.get_task(id=sys.argv[1])[1]['messageid'].strip('<>')
except KeyError:
    print(f"Task {taskno} has no messageid associated with it")
    sys.exit()

db = notmuch.Database('/home/kellya/Maildir')
threads = notmuch.Query(db, f'id:{messageid}').search_threads()
threadlist = []
for thread in threads:
    threadlist.append(thread)

threadmsgs = list(threadlist[0].get_messages())
if threadmsgs:
    themessage = list(threadmsgs[0].get_message_parts())
    print(html2text.html2text(themessage[0].get_payload()))
