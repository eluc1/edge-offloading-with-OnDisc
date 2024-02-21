import json
import threading
import requests
from concurrent.futures import ThreadPoolExecutor

# 全局变量用于线程锁
file_lock = threading.Lock()
pod_list=['192.168.63.130:8800',
'192.168.63.131:8800']

def process_line(line):
    # 在这里执行对每一行的处理逻辑，这里只是简单地打印
    line_dict = json.loads(line)
    
    ip='192.168.63.130:8800'
    predict_json = {
    "start_time": int(line_dict['time']),
    "predicted_runtime": 1,
    "time_sensitive_weight": int(line_dict['priority']) + 1,
    "task_type": int(line_dict['type']),
    "task_data": " "
    }
    response1 = requests.post(f'http://{ip}/predict', json=predict_json)
    tempdata=response1.json()
    json_data = {
        "start_time": int(line_dict['time']),
        "predicted_runtime": tempdata['predicted_runtime'],
        "time_sensitive_weight": int(line_dict['priority']) + 1,
        "task_type": int(line_dict['type']),
        "task_data": " "
    }

    response = requests.post(f'http://{ip}/process', json=json_data)
    response_time = response.elapsed.total_seconds()
        
    print(json_data)
        
    print(response1.text)
    print(response.text)
    print(response_time)
    ''''if response.status_code==200:
    	print(response.text)'''

def process_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            # 将每一行提交给线程池进行处理
            executor.submit(process_line, line)

# 设置线程池大小
pool_size = 10
# 创建线程池
with ThreadPoolExecutor(max_workers=pool_size) as executor:
    # 指定json文件路径
    json_file = 'somedata.json'
    
    # 启动一个线程处理文件，但不使用锁
    process_file(json_file)

# 注意：在实际的应用中，你可能需要根据具体需求修改process_line和process_file函数的实现。

 
