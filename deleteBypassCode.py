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
import main

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



ts= time.time()
startTime=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
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
print("Start time - " + startTime)
print("End time - " + endTime)
main.exit()