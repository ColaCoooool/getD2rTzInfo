import requests
from bs4 import BeautifulSoup
import json
import base64

class D2TerrorZoneScraper:
    def __init__(self):
        self.url = "https://d2emu.com/tz"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # 新的解密密钥，从网页JavaScript中提取
        self.key1 = "kab2jnb1"
        self.key2 = "kbd2jnb1"
    
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
            
            # 第四步：Base64编码（与JavaScript的btoa对应）
            encoded_result = base64.b64encode(result2_str.encode('utf-8')).decode('utf-8')
            
            # 第五步：再次Base64解码（与JavaScript的atob对应）
            final_data = base64.b64decode(encoded_result).decode('utf-8', errors='ignore')
            
            return final_data
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
            tz_data = {
                "current": self._extract_current_tz(soup),
                "next": self._extract_next_tz(soup)
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
                    # 提取位置信息
                    current_tz["location"] = self._extract_location(en_name)
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
            time_text = current_time_element.text.strip()
            if time_text:
                current_tz["time"] = time_text
            else:
                # 计算当前的30分钟间隔时间
                import datetime
                now = datetime.datetime.now()
                if now.minute < 30:
                    current_time = now.replace(minute=0, second=0)
                else:
                    current_time = now.replace(minute=30, second=0)
                current_tz["time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
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
                    # 提取位置信息
                    next_tz["location"] = self._extract_location(en_name)
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
            time_value = next_time_element.get("value", "")
            if time_value:
                try:
                    import datetime
                    timestamp = int(time_value)
                    next_tz["time"] = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(f"时间戳转换失败: {e}")
                    import datetime
                    next_tz["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                import datetime
                next_tz["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
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
            if "immunities:" in text.lower():
                # 提取免疫信息
                immunity_text = text.split(":")[1].strip() if ":" in text else ""
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
            "Burial Grounds": "Act 1",
            
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
        zone_parts = zone_name.split('</br>')
        for part in zone_parts:
            part = part.strip()
            for key in location_map:
                if key in part:
                    return location_map[key]
        
        # 如果没有找到，再尝试整个名称
        for key in location_map:
            if key in zone_name:
                return location_map[key]
        
        return "Unknown"

def main():
    """主函数"""
    scraper = D2TerrorZoneScraper()
    tz_data = scraper.get_tz_data()
    
    if tz_data:
        print("=== 暗黑破坏神2 恐怖地带信息 ===")
        print("\n当前恐怖地带:")
        print(json.dumps(tz_data["current"], indent=2, ensure_ascii=False))
        print("\n下场恐怖地带:")
        print(json.dumps(tz_data["next"], indent=2, ensure_ascii=False))
    else:
        print("无法获取恐怖地带信息")

if __name__ == "__main__":
    main()
