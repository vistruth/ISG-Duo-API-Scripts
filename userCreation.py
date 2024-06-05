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
from IgnoreFolder.keys import *
from itertools import repeat
import time
import datetime


'''
THIS WAS USED TO CREATE A BUNCH OF TEST USERS

'''
keyI = integration
keyS = secret


admin_api = duo_client.Admin(
    ikey=keyI,
    skey=keyS,
    host=host,
    ca_certs='DISABLE'
)
ts= time.time()
startTime=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
useridList=[]
number = '1'
for i in repeat(None, 999):
	username = "username_"
	usernameplusnumber = username+number
	repeatCreation = admin_api.json_api_call(
		 'POST',
    	'/admin/v1/users/bulk_create',
    		{
			'users':json.dumps(
				[
				{
					'username': usernameplusnumber
				}
				]
			)
			}
		)
	number = str(int(number)+1)
	pprint.pprint(repeatCreation)
	for resp in repeatCreation:
		useridList.append(resp['user_id'])
	else:
		("Can't find user_id")


print("List has been created. The list will be printed in 5 seconds")
time.sleep(5)
print(useridList)


for user_id in useridList:
	codeCreation = admin_api.json_api_call(
		"POST",
		f"/admin/v1/users/{user_id}/bypass_codes",
		{}
	)
	print(codeCreation)

ts2 = time.time()
endTime=datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
print(startTime)
print(endTime)
