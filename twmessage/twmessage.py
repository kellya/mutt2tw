#!/usr/bin/env python
import notmuch
import sys
import html2text
from taskw import TaskWarrior


def get_messageid(taskno):
    ''' Return the mail objects' unique message ID'''
    task = TaskWarrior(marshal=True)
    try:
        messageid = task.get_task(id=taskno)[1]['messageid'].strip('<>')
        return [messageid, {}]
    except KeyError:
        return [False, {'error': f'No message id found for task {taskno}'}]


def get_message(messageid):
    ''' Return the text of a message found by messageid'''
    db = notmuch.Database('/home/kellya/Maildir')
    threads = notmuch.Query(db, f'id:{messageid}').search_threads()
    threadlist = []
    for thread in threads:
        threadlist.append(thread)
    try:
        threadmsgs = list(threadlist[0].get_messages())
        themessage = list(threadmsgs[0].get_message_parts())
        # A quick and dirty check if the message is html
        if "<html>" in themessage[0].get_payload():
            # if it is HTML, convert it to text
            return html2text.html2text(themessage[0].get_payload())
        else:
            # otherwise just spit out the text
            return themessage[0].get_payload()
    except IndexError:
        return False


def main():
    messageid = get_messageid(sys.argv[1])[0]
    message = get_message(messageid)
    if message:
        print(message)
    else:
        print(f'No message found for task {sys.argv[1]}')


if __name__ == '__main__':
    main()
