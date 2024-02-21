import json  
import requests


json_data={
"start_time":1992813863543,
"predicted_runtime":2,
"time_sensitive_weight":0,
"task_type":8,
"task_data":" "
}
ip='192.168.63.130:8800'
response = requests.post(f'http://{ip}/predict',json=json_data)
response_time = response.elapsed.total_seconds()
print(response.text)
print(response_time)

