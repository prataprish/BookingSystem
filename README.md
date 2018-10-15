API documentation:
Language Used: Python
Framework Used : Django
DD used : SQLite
Functionality of product is limited to
•
•
•
•

Adding info about single screen cinema

Retrieving vacant seats in cinema

Booking seats if available

Providing the best choice of seats given number of people and any one of the preferred seat




Detailed discussion
POST/GET request from CLI or any other medium

Working examples: (in Python)

Adding info
import json

import requests

info = { "name":"inox", "seatInfo": { "A": { "numberOfSeats": 10, "aisleSeats": [0, 5 ,6, 9] }, "B":
{ "numberOfSeats": 15, "aisleSeats": [0, 5 ,6, 9] }, "D": { "numberOfSeats": 20, "aisleSeats": [0, 5 ,
6, 9] } } }

url = 'http://127.0.0.1:9090/screens/'

infoJSON = json.dumps(info)

requests.post( url, data = { 'data':infoJSON })

info = { "name":"PVR", "seatInfo": { "A": { "numberOfSeats": 10, "aisleSeats": [0, 5 ,6, 9] }, "B":
{ "numberOfSeats": 15, "aisleSeats": [0, 5 ,6, 9] }, "C": { "numberOfSeats": 20, "aisleSeats": [0, 5 ,
6, 9] } } }

infoJSON = json.dumps(info)

requests.post( url, data = { 'data':infoJSON })

Retrieving vacant seats
import json

import requests

url = ‘http://127.0.0.1:9090/screens/PVR/seats?status=unreserved’

infoJSON = json.dumps(info)

response = requests.get( url )

print(response.text)


# Output : {"A": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "B": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "C":
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]}

Booking Tickets
# On successful booking 200 status is encountered other wise 400 status
import json

import requests

info = { "seats": { "B": [1, 2], "C": [ 6, 7] } }

url = 'http://127.0.0.1:9090/screens/PVR/reserve/'

infoJSON = json.dumps(info)

res = requests.post( url, data = { 'seats':infoJSON })

print(res)

# output <Response [200]>

res = requests.post( url, data = { 'seats':infoJSON })

print(res)

# output <Response [400]>

Optimal Choice of seats
import json

import requests

url = 'http://127.0.0.1:9090/screens/PVR/seats?numSeats=2&choice=A4'

res = requests.get( url)

print(res.text)

#output [{"availableSeats": {"A": [3, 4]}}, {"availableSeats": {"A": [4, 5]}}]

url = 'http://127.0.0.1:9090/screens/PVR/seats?numSeats=5&choice=A7'

res = requests.get(url)

print(res.text)

#output []


