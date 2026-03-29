#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试解密逻辑
"""
import base64
import json

# 新的解密密钥
key1 = "kab2jnb1"
key2 = "kbd2jnb1"

def decrypt(encrypted_data):
    """解密加密的数据"""
    try:
        # 第一步：Base64解码
        decoded_data = base64.b64decode(encrypted_data).decode('utf-8', errors='ignore')
        
        # 第二步：与key1进行XOR
        result1 = []
        for i, char in enumerate(decoded_data):
            key_char = key1[i % len(key1)]
            result1.append(chr(ord(char) ^ ord(key_char)))
        result1_str = ''.join(result1)
        
        # 第三步：与key2进行XOR
        result2 = []
        for i, char in enumerate(result1_str):
            key_char = key2[i % len(key2)]
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

# 测试数据（从网页中获取的加密数据）
test_data = "eyF8aFRXIjogIVp1NTI1ZFx2MTZhZVx1NTBjMlx1Njc5NDovYnI+XHU2NDVkXHU3NmJjXHU1NzMwX3M3MjYyPC9hdD5cdTZjYmBadTZmYTRcdjM3MzBcdTdiMTQiLCAiaXdPVCI6ICJHanNuZ2xhIFNgaXJ0aWNhdHFvY2U8L2JyPVVvdHRlcnJiaGVvIFNjb3FyaWNhdG9yZjovYnI+QWJqdXNvIFBhbHZib3NvIiwgIXZ0QlIiOiAhVWVsdmEgZGx1IEVzZm9sYmJvcmVzPC9hdD5NYXNtb3F0YSBkb3MgRnVmb2xhZG9xY3M8L2JyPkVpc3NvIFBhbXJhbm9zbyIvJiJydVJVIjkmIlx1MDQxN1p1MDQzNlx2NjQ0M1x1MDc1ZFx1MDQzMFp1MDQzYlx2NjQzOCBcdTMyNDFcdTA0MDRcdTA0MzVfczA0MzZcdTMyMzVcdTA0MDRcdTA0MzBfczA0NDJcdTMyMzVcdTA0MGRcdTA0MzVfczA0Mzk8L2F0Plx1MDQxZVp1MDQzZVx2NjQzNFx1MDc1N1x1MDQzNlp1MDQzY1x2NjQzNVx1MDc1Ylx1MDQ0YFp1MDQzNSBfczA0NDFcdTMyMzJcdTA0MDNcdTA0MzZfczA0MzVcdTMyMzJcdTA0MDZcdTA0NDJfczA0MzVcdTMyM2JcdTA0MDNcdTA0Mzk/KWJyPlx1MDc3M1x1MDQzYVp1MDQ0M1x2NjQzMVx1MDc1ZVx1MDQzYlp1MDQzMFx2NjQ0ZiBcdTMyNDJcdTA0NzZcdTA0NGZfczA0NDFcdTMyMzhcdTA0MGJcdTA0MzAhKiAiZXNNWCE8ICJKdW5nb2cgZGUgbG9wJkRlc29sbGJib3JlczwvYXQ+Q2FsYWJsfG8gZGUgbGx1IERlc29sb2dkb3JlczwsZHI+Rm9zbyNWYW50YW5vcGkiLCAiZW5WVSI6ICJGbGJ/ZXIgSnVuZGplPC9icj5FamF5ZXIgRHZoZ2VvbjwvYXQ+U3dhbXB6JlBpdCIsICFtb0tSIjogIVp1YzU3ZFx2YjBjOFx1YzQ/MCBcdWJjMzZcdWI5YmM/KWJyPlx1YzYxZFx1ZDBjO1p1Yzc5MCBfc2MxOGNcdWJiNzQ8L2JyPVp1YzJiNVx2YjU1YyBcdWJiNmNcdWIzNT9cdWM3NzQhKiAiZGVERSE8ICJTY2hpbWJlcmRzY2h2aGdlbDwvYnE4U2NoaW5kZnRkdW5nZW9tOi9icj5TdW52ZmxvY2giLyYiZnJGUiI5JiJMYSBKdW1hbGUgZGUgb1p1MjAxOVx2NjBjOWNvcmBuZXVyPC9icThMYSBQcmlwaW4gZGUgbF9zMjAxOVx1MzZjOWNvcmNrY3VyPC9icj1KZSBCb3VyYW9lciIsICJzalBMIjogIkdadTAxN2N1bWFsYSBcdTAyMjF1cGllXHY2MTdjY1x1MzZmM3c8L2JxOFBvZHppZW5vYSBcdTAxNzd1cGllXHUzNzdjY1x1MDNgM3c8L2JyPURhZ2llbm5iJkN6ZWx1XHY2MTViXHUwMjY3IiwgImpiTFAiOiAiXHY1MGQ1XHUzM2NjXHUzMGE3WnUzMGU0XHY1MGZjXHUzMzBlXHU1YmM1WnU2Nzk3PCxkcj5cdTMwZzNcdTMwZWNfczMwYTRcdTA2ZTRcdTMwZWVcdTMwNmVfczU3MzBcdTdjMGJcdTcyNTQ8L2JyPlx2MGNiY1x1NTQ1MFx1MzA2Zlp1N2E3NFx2NTA1MFx1MzM+OSIsICJ6a0VOIjogIlx2MzI2NVx1NzVnZVx1OWI1N1p1NGUxYlx2MDc5NzwvYnE4XHU1MjY1X3M3NmFlXHU6ZDU0XHU3Nmc3XHU3MjYyPylicj5cdTZgZGNcdTZjZmdadTk2NzdcdjM3NTEiLCAhY3NFUyI6ICFVZWx2YSBEZnVvbGxhZG9xZzwvYnI+TWJ8bW9ycmEgZ2MgRGVzb2xvZ21pZW50bz8pYnI+Rm9zbCZQYW50YW5sdW8ifQ=="

print("测试解密逻辑...")
print(f"加密数据长度: {len(test_data)}")

decrypted = decrypt(test_data)
if decrypted:
    print("\n解密成功!")
    print(f"解密后数据:\n{decrypted}")
    
    # 尝试解析JSON
    try:
        data = json.loads(decrypted)
        print("\nJSON解析成功!")
        print(f"可用语言: {list(data.keys())}")
        
        # 显示各语言版本
        for lang, name in data.items():
            print(f"  {lang}: {name}")
    except json.JSONDecodeError as e:
        print(f"\nJSON解析失败: {e}")
else:
    print("解密失败!")
