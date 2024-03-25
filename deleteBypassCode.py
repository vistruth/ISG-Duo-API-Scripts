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
import datetime

"""
*This pulls down a list of all bypass codes and then goes through and deletes all the codes. 
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



bypassData = pd.read_csv("bypassResponse.csv")
print(bypassData)
bypassIDs = bypassData['bypass_code_id'].tolist()
codesDeleted = 0
for i in bypassIDs:
    bypassDeletion = admin_api.json_api_call(
        'DELETE',
        f"/admin/v1/bypass_codes/{i}",
        {}
    )
    pprint.pprint("Bypass code has been deleted")
    codesDeleted = codesDeleted + 1



ts2 = time.time()
endTime=datetime.datetime.fromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')

print(codesDeleted, "codes have been deleted. Application is exiting in 5 seconds")
print(startTime)
print(endTime)
time.sleep(5)
sys.exit()
   
