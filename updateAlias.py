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
