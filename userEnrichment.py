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


#adding creds and host endpoint to the admin_api variable for reference later. This code was given by duo @ this link https://duo.com/docs/adminapi#create-multiple-users scroll to the bottom on create multiple users and you'll see example code 
admin_api = duo_client.Admin(
    ikey=keyI,
    skey=keyS,
    host='INSERT API ENDPOINT',
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
print("File has been updated with all information exiting application in 5 seconds. ")


#This takes responses.csv which is the csv generated from the looped GET above and puts it in a dataframe to make life easier for data manipulation and merging
responsesDataframe = pd.read_csv('responses.csv')
#print(responsesDataframe)

#This takes in our own csv that has usernames(shortIDs) mapped to it's matching email address
externalInfoDataframe = pd.read_csv('usernamesAndEmails.csv')
#print(externalInfoDataframe)

print("Combining API data and inputted data")

#Merging the two data frames on the username value and carries over the data from each dataframe into a new dataframe
mergedDataframe = pd.merge(responsesDataframe,externalInfoDataframe, on=['username'], how='outer')

#print(mergedDataframe)

#Making a new and final data frame with email_y which is the email value from the "externalInfoDatafram.csv" the combined usernames and the user_id we get from the DUO GET request
sortedDataframe = mergedDataframe[['email_y','username','user_id']]

#Here we decide to drop all rows the contain NaN in the email_y column so that way we are only working with user_ids that we matched 
nanDrop= sortedDataframe.dropna(subset=['email_y'])


'''
The userUpdate() function loops over all the rows found in the nanDrop dataframe. 
We build out a payload inside the loop that updates with the email value found in email_y.
A POST request is sent that contains the user_id that's in the same row as the email_y that was specified.

Interesting behavior to note regarding how duo handles username aliases. If a user doesn't have any username aliases it doesn't matter what number you specify in the payload because it will just insert the alias in the first alias spot. That being said. If a user already has Alias 1 and 2 filled then DUO will respect which alias you decided to use and assign the value to the alias you selected. 

Example: TestUser1 has username alias 1 as adm_testuser1 and has alias 2 as john_doe then DUO will respect that we selected "alias 7" and assigned the email to alias 7 and skip all other aliases. That being said if TestUser2 has no username aliases then it will ignore "alias 7" and assign the email to "alias 1" 

My reason for selecting alias 7 as the deciding factor is because when you export the user list from DUO there are a few users who have up to 6 aliases for some reason. So in an attempt to not break anything I went with alias 7. That way for those who already have aliases it will assign the email as 7 and for those who don't have any it will give them "alias 1"

Also there's not rate limit for this api end point so we can let it run unattended 
'''
def userUpdate():
    for index, row in nanDrop.iterrows():
        payload =f"alias7={row['email_y']}"
        updatedUserAlias = admin_api.json_api_call(
            'POST',
            f"/admin/v1/users/{row['user_id']}",
            {
                'aliases':payload
            }
        )
        pprint.pprint(updatedUserAlias)
        



userUpdate()
#print(nanDrop)
print("Application will exit in 5 seconds, Thanks")
time.sleep(5)
sys.exit()
