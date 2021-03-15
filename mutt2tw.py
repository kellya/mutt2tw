#!/bin/env python
"""
Adds a task to taskwarrior (via a subprocess call to task
"""

import sys
import subprocess
import mailparser


def clean_subject(subject, bad_text=["fwd", "re"]):
    """Remove subject barf from a subject"""
    for word in bad_text:
        subject = subject.lower().removeprefix(f"{word.lower()}: ")
    return subject


mail = sys.stdin.read()

msg = mailparser.parse_from_string(mail)

project = "testing"
title = clean_subject(msg.subject)
subprocess.run(["/usr/local/bin/task", "add", "+work", f"project:{project}", title])
