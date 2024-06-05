from __future__ import absolute_import
from __future__ import print_function
import pprint
import sys
import json
#import pandas as pd
import csv
import base64, email.utils, hmac, hashlib, urllib
import duo_client
from six.moves import input
from keys import *
from itertools import repeat
import time
import datetime

keyI = integration
keyS = secret

admin_api = duo_client.Admin(
    ikey=keyI,
    skey=keyS,
    host=host,
    ca_certs='DISABLE'
)

userlistID = []
ts= time.time()
startTime=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
getUserList = admin_api.json_api_call(
            'GET',
            '/admin/v1/users',
            {
                'limit':'300'
            }
        )
for resp in getUserList:
		userlistID.append(resp['user_id'])
else:
	("Can't find user_id")

offsetValue='300'
for i in repeat(None, 4):
    getUserListPlusMore = admin_api.json_api_call(
        'GET',
        '/admin/v1/users',
        {
            'limit':'300',
            'offset':offsetValue
        }
        )
    for resp1 in getUserListPlusMore:
        userlistID.append(resp1['user_id'])
    else:
        ("Can't find user_id")

    offsetValue = str(int(offsetValue)+300)

codesDeleted = 0

for n in userlistID:
    deleteUser = admin_api.json_api_call(
        'DELETE',
        f"/admin/v1/users/{n}",
        {}
    )
    print("user has been deleted",deleteUser)
    codesDeleted = codesDeleted + 1

ts2 = time.time()
endTime=datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
print(codesDeleted)
print(startTime)
print(endTime)