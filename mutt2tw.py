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
        bad_text = ['fwd', 're']
    for word in bad_text:
        subject = subject.lower().removeprefix(f"{word.lower()}: ")
    return subject


# We are using <pipe-send> from mutt, so read stdin into the mail message
mail = sys.stdin.read()

# Parse the mail into a message format we can handle
msg = mailparser.parse_from_string(mail)

# default project (have to use task later to clean it up.  Yes this sucks)
project = "testing"
# TODO: Figure out if there is wome way to interactively obtain this

# Take the subject of the email, remove mail subject junk, and use as the title
title = clean_subject(msg.subject)
# process will be the list to execute the full command via subprocess
process = ["/usr/local/bin/task"]
process.append("add")
# list that defines mulitiple, default tags to associate with the task
tags = ['work', 'email']
for tag in tags:
    process.append(f'+{tag}')
process.append(f"project:{project}")
process.append(f"messageid:{msg.headers['Message-ID']}")
process.append(title)
# Actually run the command
subprocess.run(process)
# Note:  I had to do this process.append stuff because the tags kept getting
# interpreted as the description if not.  This way works though
