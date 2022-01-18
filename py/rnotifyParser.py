import praw
import sqlite3
import concurrent.futures
import requests
import json
import threading
import time
import logging
import socket
import sys


database = "./users.db"
lock_socket = None

class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

def counter():
    count = 0
    count += 1
    print(count)

def retrieveUsers():
    global userList
    con = sqlite3.connect(database, check_same_thread=False)
    cur = con.cursor()
    cur.execute("SELECT DISTINCT ID, sub, query, udid FROM users Group BY sub, query, udid ORDER BY id")
    userList = cur.fetchall()
    con.close()
    return userList


def getReddit():
    global reddit, subreddit
    reddit = praw.Reddit(client_id='', client_secret='',
                         password='notifire123', user_agent='',
                         username='')
    subreddit = reddit.subreddit("all")
    return subreddit


def createAllStream(subreddit): 
    stream = subreddit.stream.submissions()
    return stream


def parseSubmission(submission):
    userList = retrieveUsers()
    subTitle_normal = submission.title.lower()
    display = submission.subreddit.display_name.lower()
    for user in userList:
        search_str = user[2].lower()
        if user[1].lower() == display and search_str in subTitle_normal:
            print("Sending Notifcation", submission.title, user[3])
            postNotif(submission.title, submission.shortlink, user[3])


def postNotif(title, shortlink,  userUUID):
    url = "https://onesignal.com/api/v1/notifications"
    data = {"app_id": "",
            "filters": [
                {"field": "tag", "key": "uuid", "relation": "=", "value": userUUID}
                ],
            "contents": {"en": shortlink},
            "headings": {"en": title},
            "data": {"title": title, "body": shortlink},
            "mutable_content": "true"}
    data_json = json.dumps(data)
    headers = {"Content-type": "application/json; charset=utf-8",
               "Authorization": "Basic "}
    r = requests.post(url, data=data_json, headers=headers)
    print(r.status_code, r.reason, r.text)



def main():
    global userList
    stream = createAllStream(getReddit())
    executor = concurrent.futures.ProcessPoolExecutor(10)
    futures = [executor.submit(parseSubmission, submission) for submission in stream]
    concurrent.futures.as_completed(futures)


if __name__ == "__main__":
    main()
