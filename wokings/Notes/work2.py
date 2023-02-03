import ast
import requests
import json
import pandas as pd
import time
import numpy as np
#
DB_url = 'http://192.168.102.155:5000/dbpotw'
DBheaders = {
    'Content-Type': 'application/json',
    'authToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzUyNTIwNDIsImlhdCI6MTY3NTE2NTY0MiwiYnJhbmNoX2lkIjoibWFpbl9tYXN0ZXIifQ.omlR7gU6UbmBZSx7OW4FgQ4wcf4DRHvTD_3GdIHo__8'
}

# st=time.time()
req = requests.request("POST", DB_url, headers=DBheaders)
st=time.time()
data = req.json()

# print(data['data'])



# a = eval(data)
# data1=json.dumps(data)
# a=json.loads(data1)

# print(type(a),type(data))


df = pd.DataFrame(data['data']).to_numpy()
# print(df)
#
#
et=time.time()
# print(df[:,13],df.shape)
#
#
print('time',et-st)



