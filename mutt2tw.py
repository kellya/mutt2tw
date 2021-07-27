#!/bin/env python
"""
Adds a task to taskwarrior (via a subprocess call to task
"""

import sys
import subprocess
import mailparser


def clean_subject(subject, bad_text=None):
    """Remove subject barf from a subject"""
    if not bad_text:
        bad_text = ["fwd", "re"]
    for word in bad_text:
        subject = subject.lower().removeprefix(f"{word.lower()}: ")
    return subject


# We are using <pipe-send> from mutt, so read stdin into the mail message
mail = sys.stdin.read()

# Parse the mail into a message format we can handle
msg = mailparser.parse_from_string(mail)

# default project (have to use task later to clean it up.  Yes this sucks)
project = "email-task"
# TODO: Figure out if there is wome way to interactively obtain this

# Take the subject of the email, remove mail subject junk, and use as the title
title = clean_subject(msg.subject)
# process will be the list to execute the full command via subprocess
process = ["/usr/local/bin/task"]
process.append("add")
# list that defines mulitiple, default tags to associate with the task
tags = ["work", "email"]
for tag in tags:
    process.append(f"+{tag}")
process.append(f"project:{project}")
# Since sometimes the header is Message-ID and other times it is Message-Id
# this stupid for loop figures out which one it is and sets that as the key
# there must be a more condensed pythonic way to accomplish this though
for key in msg.headers:
    if "message-id" == key.lower():
        message_id = key
        break
process.append(f"messageid:{msg.headers[message_id]}")
process.append("--")
process.append(title)
# Actually run the command
subprocess.run(process)
# Note:  I had to do this process.append stuff because the tags kept getting
# interpreted as the description if not.  This way works though
