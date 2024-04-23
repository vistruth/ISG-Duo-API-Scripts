from __future__ import absolute_import
from __future__ import print_function
import duo_client
import pprint
from six.moves import input
from keys import *
from itertools import repeat
import time
import sys
import pandas as pd

#Initializing credentials and hosted point. keyI and keyS are stored in a separate file called keys.py
keyI = integration
keyS = secret
apiHost = host


#adding creds and host endpoint to the admin_api variable for reference later. This code was given by duo @ this link https://duo.com/docs/adminapi#create-multiple-users scroll to the bottom on create multiple users and you'll see example code 
admin_api = duo_client.Admin(
    ikey=keyI,
    skey=keyS,
    host=apiHost,
    ca_certs='DISABLE'
)




#A lot is going on gere but the general gist is get users api call has a rate limit of 300 users per call. If you want more users you need to set an offset. I did the math for 65k users. We need to repeat a + 300 offset 219 times. We're also appending a blank CSV so we can store the values for later. 
def getUserPlusOffset():
    #initial offset this will get manipulated later on 
    offsetValue = '300'


    #creation of the csv file
    csv_filename='responses.csv'
    
    #opening csv and setting it to append mode so we can continuously update it each loop. Also set the desired column name of just general relevant information. We could just settle for "username" and "user_id" but i wanted to see what data I could pull
    with open(csv_filename, mode='a', newline="") as file:
        fieldnames = ['firstname', 'lastname', 'email', 'username', 'user_id','fullname'] 
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell()==0:
            writer.writeheader()
        
        
        #this is the initial GET request the pulls the first 300 users
        getUserList = admin_api.json_api_call(
            'GET',
            '/admin/v1/users',
            {
                'limit':'300'
            }
        )
        
        #now we loop over all the values in getUserList and start to fill the csv rows
        for resp in getUserList:
            row = {
                'firstname': resp['firstname'],
                'lastname': resp['lastname'],
                'email': resp['email'],
                'username': resp['username'],
                'fullname': resp['realname'],
                'user_id': resp['user_id']
            }
            writer.writerow(row)
            #status update 
            print(f"CSV file '{csv_filename}' has been updated.")
        
        
        #Now we're doing the same get request but we have a new param of "offset" and at the end of each iteration through the loop it adds 300 so we can increase the offset by 300 every time the loop runs. 300 * 219 = 65700 which is more than the amount of users we currently have but it's okay it won't break anything
        for i in repeat(None, 219):
            getUserListPlusOffset = admin_api.json_api_call(
                'GET',
                '/admin/v1/users',
                {
                    'limit':'300',
                    'offset': offsetValue
                }
            )
            
            for resp1 in getUserListPlusOffset:
                row = {
                    'firstname': resp1['firstname'],
                    'lastname': resp1['lastname'],
                    'email': resp1['email'],
                    'username': resp1['username'],
                    'fullname': resp1['realname'],
                    'user_id': resp1['user_id']
                }
                writer.writerow(row)
            print(f"CSV file '{csv_filename}' has been updated with offset data.")
            
            offsetValue = str(int(offsetValue)+300)
            

getUserPlusOffset()


#Another status update
print("File has been updated with all information.")
