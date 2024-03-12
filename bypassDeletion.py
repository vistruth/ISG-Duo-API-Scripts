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
from keys import *
from itertools import repeat
import pandas as pd
import time
import csv

"""
*This pulls down a list of all bypass codes and then goes through and deletes all the codes. 
*This needs to be expanded some more so that it deals with the 500 user limit and if we want we can work in some filtering logic into it. 
*That's all for now though 
"""



keyI = integration
keyS = secret


admin_api = duo_client.Admin(
    ikey=keyI,
    skey=keyS,
    host='api-302859b9.duosecurity.com',
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

        for i in repeat(None, 130):
            getBypassListPlusOffset = admin_api.json_api_call(
                'GET',
                '/admin/v1/bypass_codes',
                {
                    'limit':'500',
                    'offset': offSetValue
                }
            )

            for resp1 in getBypassListPlusOffset:
                row = {
                    
                'firstname': resp['user']['firstname'],
                'lastname': resp['user']['lastname'],
                'username': resp['user']['username'],
                'fullname': resp['user']['realname'],
                'bypass_code_id': resp['bypass_code_id']
                }
            writer.writerow(row)
            bypass_code_id = resp['bypass_code_id']
            full_name = resp['user']['realname']
            bypass_code_ids[full_name]= bypass_code_id
                
            bypasslist.append(resp['bypass_code_id'])
            print(f"CSV file '{csv_filename}' has been updated with offset data." )

            offSetValue = str(int(offSetValue)+500)


getBypassPlusOffset()

print("Files have been updated with all the needed information. Please validate the csv. Application is exiting in 5 seconds")
time.sleep(5)
sys.exit()
    
    
'''
    bypass_removal=[]
    for code in bypasslist:
        bypass_removal.append(admin_api.json_api_call(
            'DELETE',
            f'/admin/v1/bypass_codes/{code}',
            {}
            ))    
        pprint.pprint(bypass_removal)



    print(bypass_code_ids)
    


    create_code = admin_api.json_api_call(
        'POST',
        '/admin/v1/users/[user_id]/bypass_codes'
                                        
                            )

'''