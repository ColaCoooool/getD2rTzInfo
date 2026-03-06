import requests
import json

# 获取恐怖地带数据
response = requests.get('http://localhost:15554/api/terror-zones')
if response.status_code == 200:
    data = response.json()
    print("当前恐怖地带:")
    print(json.dumps(data['current'], ensure_ascii=False, indent=2))
    print("\n下场恐怖地带:")
    print(json.dumps(data['next'], ensure_ascii=False, indent=2))
else:
    print(f"获取数据失败: {response.status_code}")
