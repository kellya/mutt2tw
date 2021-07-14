# Overview
The basic idea is that we will take the subject of a message in mutt, and pass
that to taskwarrior as the description (mutt2tw).

Rather than keep the entire
message (and figure out how to parse all the various crazy things that can be
added to an email message), we rely on notmuch to do the indexing of all that
mail content.  Then we just search for that messageID in notmuch, and print out
the message associated with a task (twmessage)

# mutt2tw
Process a mail message (through pipe) from mutt, convert the subject to the task title and run system's task command to append it to your taskwarrior

# twmessage
Return message contents of a message associated with a task by searching for
taskid

# Addtional setup required
Add the following lines to your ~/.taskrc file:
```
uda.messageid.type=string
uda.messageid.label=Message-ID
```
This will allow the association of the mail's messageID with a task so we may
retrieve the details later.

# Feature Roadmap/self-wishlist
I am just starting with mutt.  One of the things I want to do is more interactively run this script to ask for things like projects, more details, etc.  I don't know if that's possible.
