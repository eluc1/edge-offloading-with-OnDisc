import json
import threading
import requests
from concurrent.futures import ThreadPoolExecutor,as_completed

# 全局变量用于线程锁
file_lock = threading.Lock()
pod_list=['192.168.63.130:8800',
'192.168.63.131:8800']
def predict_runtime(ip, line_dict):
    try:
        predict_json = {
            "start_time": int(line_dict['time']),
            "predicted_runtime": 1,
            "time_sensitive_weight": int(line_dict['priority']) + 1,
            "task_type": int(line_dict['type']),
            "task_data": " "
        }
        response = requests.post(f'http://{ip}/predict', json=predict_json, timeout=0.2)
        response.raise_for_status()  # 如果响应状态码不是 200，则会抛出异常
        print(response.json())
        return ip, response.json()
    except requests.exceptions.Timeout:
        print(f"Request to {ip} timed out")
        return ip, None  # 返回 None 表示请求超时
    except requests.exceptions.RequestException as e:
        print(f"Request to {ip} failed: {e}")
        return ip, None  # 返回 None 表示请求失败
def process_line(line):
    # 在这里执行对每一行的处理逻辑，这里只是简单地打印
    line_dict = json.loads(line)
    completed_results = []
    with ThreadPoolExecutor(max_workers=len(pod_list)) as executor:
        # 提交每个IP的预测任务
        future_to_ip = {executor.submit(predict_runtime, ip, line_dict): ip for ip in pod_list}
        # 等待所有任务完成
        print("done")
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            print(ip)
            try:
                result = future.result()  # 获取任务的结果
                # 在这里处理结果
                if result is not None:
                    print(f"Task completed for {ip}: {result}")
                    completed_results.append(result)
                else:
                    print(f"Task timed out for {ip}")
            except Exception as e:
                print(f"Task failed for {ip}: {e}")
         # 打印所有已完成任务的结果
        print(completed_results)

        # 从所有已完成任务结果中选择 WRT 最小的一个
        min_wrt_result = min(completed_results, key=lambda x: x[1]['WRT'])
        min_wrt_ip, min_wrt_data = min_wrt_result
        min_wrt, predicted_runtime = min_wrt_data['WRT'], min_wrt_data['predicted_runtime']
        
        print(min_wrt_ip)
        print(predicted_runtime)

        # 使用IP和predicted_runtime进行后续处理
        json_data = {
            "start_time": int(line_dict['time']),
            "predicted_runtime": predicted_runtime,
            "time_sensitive_weight": int(line_dict['priority']) + 1,
            "task_type": int(line_dict['type']),
            "task_data": " "
        }
        print(json_data)
        response = requests.post(f'http://{min_wrt_ip}/process', json=json_data)
        response_time = response.elapsed.total_seconds()
        
        
        
        print(f"MINWRT:{min_wrt}")
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

 
