from __future__ import absolute_import
from __future__ import print_function
import pprint
import sys
import json
import pandas as pd
import csv
import base64, email.utils, hmac, hashlib, urllib
import duo_client
from six.moves import input
from IgnoreFolder.keys import *
from itertools import repeat
import pandas as pd
import time
import csv
import datetime

"""
*This pulls down a list of all bypass codes and creates a CSV
"""

keyI = integration
keyS = secret


admin_api = duo_client.Admin(
    ikey=keyI,
    skey=keyS,
    host=host,
    ca_certs='DISABLE'
)

"""
* Make this loop 130 time so that it can get all the users in our org
* Also make the loop update the CSV each time
* 65k users / 500 users per search = 130 request offset by 500 each time 
"""


def getBypassPlusOffset():
    offSetValue='500'
    
    csv_filename='bypassResponse.csv'
   
    """
    *opening csv and setting it to append mode so we can continuously update it each loop.
    """
    bypasslist=[]
    with open(csv_filename, mode='a', newline="") as file:
        fieldnames = ['firstname', 'lastname', 'username', 'bypass_code_id','userid']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell()==0:
            writer.writeheader()

        # * First request to get the initial 500 and then we'll have a loop that gets the rest
        getBypassList = admin_api.json_api_call(
            'GET',
            '/admin/v1/bypass_codes',
            {
                'limit':'500'
            }
        )

        pprint.pprint(getBypassList)

        bypass_code_ids={}
    
        for resp in getBypassList:
            row = {        
                'firstname': resp['user']['firstname'],
                'lastname': resp['user']['lastname'],
                'username': resp['user']['username'],
                'userid': resp['user']['user_id'],
                'bypass_code_id': resp['bypass_code_id']
            }
            writer.writerow(row)
            bypass_code_id = resp['bypass_code_id']
            userid = resp['user']['user_id']
            bypass_code_ids[userid]= bypass_code_id
                
            bypasslist.append(resp['bypass_code_id'])
                
            print(f"CSV file '{csv_filename}' has been created successfully.")
            

        for i in repeat(None, 1):
            getBypassListPlusOffset = admin_api.json_api_call(
                'GET',
                '/admin/v1/bypass_codes',
                {
                    'limit':'500',
                    'offset': offSetValue
                }
            )
            pprint.pprint(getBypassListPlusOffset)
            for resp1 in getBypassListPlusOffset:
                row = {
                    
                'firstname': resp1['user']['firstname'],
                'lastname': resp1['user']['lastname'],
                'username': resp1['user']['username'],
                'userid': resp1['user']['user_id'],
                'bypass_code_id': resp1['bypass_code_id']
                }
                writer.writerow(row)
                bypass_code_id = resp1['bypass_code_id']
                full_name = resp1['user']['realname']
                bypass_code_ids[full_name]= bypass_code_id
                    
                bypasslist.append(resp1['bypass_code_id'])
                print(f"CSV file '{csv_filename}' has been updated with offset data." )

            offSetValue = str(int(offSetValue)+500)


getBypassPlusOffset()
print("List of bypass codes has been generated and saved to bypassResponse.csv. Please move over to the bypassDeletion.py script to delete the list of bypass codes. Script will close in 5 seconds")
time.sleep(5)
sys.exit()