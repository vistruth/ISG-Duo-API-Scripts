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

'''
This pulls down a list of all bypass codes and then goes through and deletes all the codes. This needs to be expanded some more so that it deals with the 500 user limit and if we want we can work in some filtering logic into it. That's all for now though 
'''



keyI = integration
keyS = secret


admin_api = duo_client.Admin(
    ikey=keyI,
    skey=keyS,
    host='INSERT API ENDPOINT',
    ca_certs='DISABLE'
)

response = admin_api.json_api_call(
    'GET',
    '/admin/v1/bypass_codes',
    {
        'limit':'500'
    }
)

pprint.pprint(response)

csv_filename='responses.csv'
bypass_code_ids={}

bypasslist=[]
with open(csv_filename, mode='w', newline="") as file:
    fieldnames = ['firstname', 'lastname', 'email', 'username', 'bypass_code_id','fullname']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for resp in response:
        row = {
            
            'firstname': resp['user']['firstname'],
            'lastname': resp['user']['lastname'],
            'email': resp['user']['email'],
            'username': resp['user']['username'],
            'fullname': resp['user']['realname'],
            'bypass_code_id': resp['bypass_code_id']
        }
        writer.writerow(row)
        bypass_code_id = resp['bypass_code_id']
        full_name = resp['user']['realname']
        bypass_code_ids[full_name]= bypass_code_id
        
        bypasslist.append(resp['bypass_code_id'])
        
print(f"CSV file '{csv_filename}' has been created successfully.")
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
'''


create_code = admin_api.json_api_call(
    'POST',
    '/admin/v1/users/[user_id]/bypass_codes'
                                    
                          )

