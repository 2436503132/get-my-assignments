import json

import requests
from typing import List

url = 'https://app.schoology.com/home/upcoming_ajax'

# sid = input("SESSION id: ")
# value = input("Value: ")
sid = 'SESSa4c564b873aecda55b12a530bf2ece51'
value = '28a7b23940febe0ec7100afd37849ea9'
cookies = {sid: value}
input()

response = requests.get(url, cookies=cookies)
try:
    data = json.loads(response.text)
except:
    print("Error: Could not login successfully.")
    exit()

body: str = data['html']

events: List[str] = body.split("upcoming-event")

global_time: str = ''
first = 'https://app.schoology.com'


class Event:
    def __init__(self, type: str, course: str, href: str, title: str, due: str):
        self.type = type
        self.course = course
        self.href = href
        self.title = title
        self.due = due

    def __str__(self):
        return f"{self.type} in {self.course}: {self.title}. Due date: {self.due}, url: {first + self.href}"


event_list: List[Event] = []

for e in events:
    arr = e.split("date-header")
    if len(arr) == 2:
        global_time = arr[1].split('><h4>')[1].split("</h4>")[0]
    arr = e.split("aria-label='")
    if len(arr) != 2:
        continue
    whole = arr[1]
    course = whole.split("'><")[0]
    evt = whole.split('"visually-hidden">')[1].split('.<')[0]
    whole = whole.split('</span></span><a href="')[1]
    href = whole.split('"')[0]
    title = whole.split('>')[1].split('</a')[0]

    arr = whole.split('upcoming-time')
    if len(arr) == 2:
        due = arr[1].split("'>")[1].split('<')[0]
        event = Event(evt, course, href, title, global_time + due)
    else:
        due = "N/A"
        event = Event(evt, course, href, title, due)

    event_list.append(event)

for e in event_list:
    print(e)
