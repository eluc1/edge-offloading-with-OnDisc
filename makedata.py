import json

json_file_path = 'somedata.json'
temp_json_file_path = 'temp_json_file.json'

# 逐行处理 JSON 文件
with open(json_file_path, 'r') as infile, open(temp_json_file_path, 'w') as outfile:
    for line in infile:
        line=line.strip()
        # 解析 JSON 对象
        entry = json.loads(line)

        # 将 'priority' 字段的值转换为整数并加一
        entry['priority'] = str(int(entry['priority']) + 1)

        # 将修改后的 JSON 对象写入临时文件中
        json.dump(entry, outfile)
        outfile.write('\n')

# 删除源文件
import os
os.remove(json_file_path)

# 重命名临时文件为源文件
os.rename(temp_json_file_path, json_file_path)

