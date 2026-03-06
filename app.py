from flask import Flask, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import base64
import json
import time
import schedule
import threading
import datetime

app = Flask(__name__)

# 数据存储文件路径
HISTORY_FILE = 'tz_history.json'

class D2TerrorZoneScraper:
    def __init__(self):
        self.url = "https://d2emu.com/tz"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # 解密密钥，从网页JavaScript中提取
        self.key1 = "ka02jnb1"
        self.key2 = "kb32jnb1"
    
    def decrypt(self, encrypted_data):
        """解密加密的数据"""
        try:
            # 第一步：Base64解码
            decoded_data = base64.b64decode(encrypted_data).decode('utf-8', errors='ignore')
            
            # 第二步：与key1进行XOR
            result1 = []
            for i, char in enumerate(decoded_data):
                key_char = self.key1[i % len(self.key1)]
                result1.append(chr(ord(char) ^ ord(key_char)))
            result1_str = ''.join(result1)
            
            # 第三步：与key2进行XOR
            result2 = []
            for i, char in enumerate(result1_str):
                key_char = self.key2[i % len(self.key2)]
                result2.append(chr(ord(char) ^ ord(key_char)))
            result2_str = ''.join(result2)
            
            return result2_str
        except Exception as e:
            print(f"解密失败: {e}")
            return None
    
    def get_tz_data(self):
        """获取恐怖地带数据"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取数据
            current_tz = self._extract_current_tz(soup)
            next_tz = self._extract_next_tz(soup)
            
            print(f"Debug - get_tz_data current_tz: {current_tz}")
            print(f"Debug - get_tz_data next_tz: {next_tz}")
            
            tz_data = {
                "current": current_tz,
                "next": next_tz
            }
            
            return tz_data
        except Exception as e:
            print(f"获取数据失败: {e}")
            return None
    
    def _extract_current_tz(self, soup):
        """提取当前恐怖地带信息"""
        current_tz = {
            "name": "",
            "immunities": [],
            "location": "",
            "time": ""
        }
        
        # 查找当前恐怖地带的span元素
        current_element = soup.find(id="__1")
        if current_element:
            # 提取value属性中的加密数据
            value = current_element.get("value", "")
            
            # 解密数据
            decrypted_data = self.decrypt(value)
            if decrypted_data:
                try:
                    # 解析JSON数据
                    data = json.loads(decrypted_data)
                    # 提取中文场景名称，优先使用简体中文
                    if "zhCN" in data:
                        current_tz["name"] = data["zhCN"]
                    elif "zhTW" in data:
                        current_tz["name"] = data["zhTW"]
                    elif "enUS" in data:
                        current_tz["name"] = data["enUS"]
                    else:
                        # 取第一个可用的语言版本
                        for lang, name in data.items():
                            current_tz["name"] = name
                            break
                    
                    # 提取英文场景名称用于位置匹配
                    en_name = data.get("enUS", current_tz["name"])
                    # 打印调试信息
                    print(f"Debug - current_tz name: {current_tz['name']}")
                    print(f"Debug - en_name: {en_name}")
                    # 提取位置信息
                    current_tz["location"] = self._extract_location(en_name)
                    print(f"Debug - current_tz location: {current_tz['location']}")
                except Exception as e:
                    print(f"解析JSON失败: {e}")
                    current_tz["name"] = decrypted_data[:100]
                    # 尝试使用原始名称提取位置信息
                    current_tz["location"] = self._extract_location(current_tz["name"])
        else:
            # 提取位置信息
            current_tz["location"] = self._extract_location(current_tz["name"])
        
        # 提取时间信息
        current_time_element = soup.find(id="current-time")
        if current_time_element:
            # 打印元素内容以便调试
            print(f"Current time element: {current_time_element}")
            print(f"Current time text: {current_time_element.text.strip()}")
            # 尝试从元素内容或属性中提取时间
            time_text = current_time_element.text.strip()
            if time_text:
                current_tz["time"] = time_text
            else:
                # 从网页JavaScript逻辑分析，当前时间是基于当前时间计算的
                # 网页中使用了类似的逻辑：new Date().setMinutes(new Date().getMinutes() < 30 ? 0 : 30), setSeconds(0)
                import datetime
                now = datetime.datetime.now()
                # 计算当前的30分钟间隔时间
                if now.minute < 30:
                    current_time = now.replace(minute=0, second=0)
                else:
                    current_time = now.replace(minute=30, second=0)
                current_tz["time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            print("Current time element not found")
            # 如果元素不存在，使用当前时间
            import datetime
            current_tz["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 提取免疫信息
        current_tz["immunities"] = self._extract_immunities(soup)
        
        return current_tz
    
    def _extract_next_tz(self, soup):
        """提取下场恐怖地带信息"""
        next_tz = {
            "name": "",
            "immunities": [],
            "location": "",
            "time": ""
        }
        
        # 查找下场恐怖地带的span元素
        next_element = soup.find(id="__2")
        if next_element:
            # 提取value属性中的加密数据
            value = next_element.get("value", "")
            
            # 解密数据
            decrypted_data = self.decrypt(value)
            if decrypted_data:
                try:
                    # 解析JSON数据
                    data = json.loads(decrypted_data)
                    # 提取中文场景名称，优先使用简体中文
                    if "zhCN" in data:
                        next_tz["name"] = data["zhCN"]
                    elif "zhTW" in data:
                        next_tz["name"] = data["zhTW"]
                    elif "enUS" in data:
                        next_tz["name"] = data["enUS"]
                    else:
                        # 取第一个可用的语言版本
                        for lang, name in data.items():
                            next_tz["name"] = name
                            break
                    
                    # 提取英文场景名称用于位置匹配
                    en_name = data.get("enUS", next_tz["name"])
                    # 打印调试信息
                    print(f"Debug - next_tz name: {next_tz['name']}")
                    print(f"Debug - en_name: {en_name}")
                    print(f"Debug - data: {data}")
                    # 提取位置信息
                    next_tz["location"] = self._extract_location(en_name)
                    print(f"Debug - next_tz location: {next_tz['location']}")
                except Exception as e:
                    print(f"解析JSON失败: {e}")
                    next_tz["name"] = decrypted_data[:100]
                    # 尝试使用原始名称提取位置信息
                    next_tz["location"] = self._extract_location(next_tz["name"])
        else:
            # 提取位置信息
            next_tz["location"] = self._extract_location(next_tz["name"])
        
        # 提取时间信息
        next_time_element = soup.find(id="next-time")
        if next_time_element:
            # 打印元素内容以便调试
            print(f"Next time element: {next_time_element}")
            print(f"Next time text: {next_time_element.text.strip()}")
            # 尝试从value属性中提取Unix时间戳
            time_value = next_time_element.get("value", "")
            if time_value:
                try:
                    import datetime
                    timestamp = int(time_value)
                    next_tz["time"] = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(f"时间戳转换失败: {e}")
                    # 如果转换失败，使用当前时间
                    import datetime
                    next_tz["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                # 如果没有时间值，使用当前时间
                import datetime
                next_tz["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            print("Next time element not found")
            # 如果元素不存在，使用当前时间
            import datetime
            next_tz["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 提取免疫信息
        next_tz["immunities"] = self._extract_immunities(soup)
        
        return next_tz
    
    def _extract_immunities(self, soup):
        """提取场景的属性免疫信息"""
        immunities = []
        
        # 查找包含免疫信息的tooltip元素
        tooltip_elements = soup.find_all(class_="tooltip-text")
        for tooltip in tooltip_elements:
            text = tooltip.text.strip()
            if "immunities:" in text:
                # 提取免疫信息
                immunity_text = text.split("immunities:")[1].strip()
                # 分割免疫属性
                immunity_list = immunity_text.split(",")
                for imm in immunity_list:
                    imm = imm.strip()
                    if imm:
                        immunities.append(imm)
                break
        
        return immunities
    
    def _extract_location(self, zone_name):
        """提取场景的位置信息"""
        # 根据场景名称返回位置信息
        # 这里可以根据实际需要扩展位置信息数据库
        location_map = {
            # Act 1
            "Cold Plains": "Act 1",
            "Stony Field": "Act 1",
            "Darkwood": "Act 1",
            "Black Marsh": "Act 1",
            "Tristram": "Act 1",
            "Cathedral": "Act 1",
            "Catacombs": "Act 1",
            "Cave": "Act 1",
            "Underground Passage": "Act 1",
            "Forgotten Tower": "Act 1",
            "Jail": "Act 1",
            "Barracks": "Act 1",
            "Pit": "Act 1",
            "Mausoleum": "Act 1",
            "Crypt": "Act 1",
            "Blood Moor": "Act 1",
            "Den of Evil": "Act 1",
            
            # Act 2
            "Far Oasis": "Act 2",
            "Lost City": "Act 2",
            "Ancient Tunnels": "Act 2",
            "Stony Tomb": "Act 2",
            "Rocky Waste": "Act 2",
            "Tal Rasha's Tombs": "Act 2",
            "Lut Gholein Sewers": "Act 2",
            "Dry Hills": "Act 2",
            "Halls of the Dead": "Act 2",
            "Claw Viper Temple": "Act 2",
            "Arcane Sanctuary": "Act 2",
            "Canyon of the Magi": "Act 2",
            "Sewers": "Act 2",
            "Palace Cellar": "Act 2",
            
            # Act 3
            "Travincal": "Act 3",
            "Kurast Bazaar": "Act 3",
            "Temples": "Act 3",
            "Durance of Hate": "Act 3",
            "Flayer Jungle": "Act 3",
            "Spider Forest": "Act 3",
            "Great Marsh": "Act 3",
            "Swampy Pit": "Act 3",
            "Kurast Causeway": "Act 3",
            
            # Act 4
            "Bloody Foothills": "Act 4",
            "Frigid Highlands": "Act 4",
            "Abaddon": "Act 4",
            "Outer Steppes": "Act 4",
            "Plains of Despair": "Act 4",
            "City of the Damned": "Act 4",
            "River of Flame": "Act 4",
            "Chaos Sanctuary": "Act 4",
            
            # Act 5
            "Arreat Plateau": "Act 5",
            "Bloody Foothills": "Act 5",
            "Frigid Highlands": "Act 5",
            "Abaddon": "Act 5",
            "Crystalline Passage": "Act 5",
            "Frozen River": "Act 5",
            "Glacial Trail": "Act 5",
            "Drifter Cavern": "Act 5",
            "Ancient's Way": "Act 5",
            "Icy Cellar": "Act 5",
            "Nihlathak's Temple": "Act 5",
            "Worldstone Keep": "Act 5",
            "Throne of Destruction": "Act 5",
            "Worldstone Chamber": "Act 5",
            "Halls of Vaught": "Act 5",
            "Pit of Acheron": "Act 5",
            
            # 中文场景名称映射
            "干燥高地": "Act 2",
            "亡者大殿": "Act 2",
            "外域荒原": "Act 4",
            "绝望平原": "Act 4",
            "先祖之路": "Act 5",
            "寒冰地窖": "Act 5",
            "鲜血荒地": "Act 1",
            "邪恶洞穴": "Act 1",
            "亚瑞特高原": "Act 5",
            "阿克隆深渊": "Act 5"
        }
        
        # 查找场景名称中的主要部分
        # 处理包含多个场景的情况（如"Blood Moor</br>Den of Evil"）
        print(f"Debug - zone_name: {zone_name}")
        zone_parts = zone_name.split('</br>')
        print(f"Debug - zone_parts: {zone_parts}")
        for part in zone_parts:
            part = part.strip()
            print(f"Debug - part: {part}")
            for key in location_map:
                if key in part:
                    print(f"Debug - found key: {key}")
                    return location_map[key]
        
        # 如果没有找到，再尝试整个名称
        for key in location_map:
            if key in zone_name:
                return location_map[key]
        
        return "Unknown"

# 创建全局实例
scraper = D2TerrorZoneScraper()

# 数据管理函数
def load_history():
    """加载历史记录"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('records', [])
    except Exception as e:
        print(f"加载历史记录失败: {e}")
        return []

def save_history(records):
    """保存历史记录"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({'records': records}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存历史记录失败: {e}")
        return False

def cleanup_history():
    """清理过期记录，只保留最近24小时的"""
    records = load_history()
    current_time = datetime.datetime.now()
    cutoff_time = current_time - datetime.timedelta(hours=24)
    
    # 过滤出24小时内的记录
    recent_records = [record for record in records if 
                     datetime.datetime.fromisoformat(record['timestamp']) > cutoff_time]
    
    # 保存清理后的记录
    save_history(recent_records)
    print(f"清理历史记录，保留 {len(recent_records)} 条记录")

def record_terror_zone():
    """记录当前恐怖地带"""
    print("开始记录恐怖地带...")
    try:
        # 获取当前恐怖地带数据
        tz_data = scraper.get_tz_data()
        if tz_data and tz_data.get('current'):
            current_tz = tz_data['current']
            
            # 创建记录
            record = {
                'timestamp': datetime.datetime.now().isoformat(),
                'name': current_tz.get('name', ''),
                'location': current_tz.get('location', ''),
                'immunities': current_tz.get('immunities', []),
                'time': current_tz.get('time', '')
            }
            
            # 加载历史记录
            records = load_history()
            
            # 检查是否已存在相同时间和场景的记录
            existing_record = False
            for r in records:
                if r['time'] == record['time'] and r['name'] == record['name']:
                    existing_record = True
                    break
            
            # 只有当不存在相同记录时才添加
            if not existing_record:
                records.append(record)
                print(f"添加新记录: {current_tz.get('name', '未知')} - {current_tz.get('time', '未知时间')}")
            else:
                print(f"记录已存在，跳过: {current_tz.get('name', '未知')} - {current_tz.get('time', '未知时间')}")
            
            # 清理过期记录
            current_time = datetime.datetime.now()
            cutoff_time = current_time - datetime.timedelta(hours=24)
            recent_records = [r for r in records if 
                             datetime.datetime.fromisoformat(r['timestamp']) > cutoff_time]
            
            # 保存记录
            if save_history(recent_records):
                print(f"成功保存记录，当前共 {len(recent_records)} 条")
            else:
                print("保存记录失败")
        else:
            print("获取恐怖地带数据失败")
    except Exception as e:
        print(f"记录恐怖地带失败: {e}")

def run_scheduled_tasks():
    """运行定时任务"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

# 设置定时任务
schedule.every().hour.at(":03").do(record_terror_zone)
schedule.every().hour.at(":33").do(record_terror_zone)
schedule.every().day.at("00:00").do(cleanup_history)

# 启动定时任务线程
task_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
task_thread.start()
print("定时任务已启动")

# 启动时先获取一次恐怖地带数据
print("启动时获取初始恐怖地带数据...")
record_terror_zone()

@app.route('/api/terror-zones', methods=['GET'])
def get_terror_zones():
    """获取恐怖地带信息的API接口"""
    tz_data = scraper.get_tz_data()
    print(f"Debug - get_terror_zones tz_data: {tz_data}")
    if tz_data:
        return jsonify(tz_data)
    else:
        return jsonify({"error": "无法获取恐怖地带信息"}), 500

@app.route('/', methods=['GET'])
def serve_index():
    """提供首页"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    """提供静态文件"""
    return send_from_directory('.', path)

@app.route('/api/tz-history', methods=['GET'])
def get_tz_history():
    """获取恐怖地带历史记录"""
    try:
        records = load_history()
        # 按时间倒序排序
        records.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify({'records': records})
    except Exception as e:
        print(f"获取历史记录失败: {e}")
        return jsonify({'records': []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15554, debug=False)
