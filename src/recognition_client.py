# client.py

import time
import requests
import os
from music21 import converter
import json


def run_recognition(image_path):
    """
    输入本地 PNG 图片路径，发送到远程服务识别五线谱，生成 krn 和 midi 文件。
    """
    res_path = r'F:/Graduation Design/StaveRecognition/midi_file/'
    os.makedirs(res_path, exist_ok=True)

    with open(image_path, 'rb') as f:
        files = {
            'file': ('input.png', f, 'image/png')
        }
        data = {
            'ocr_type': 'format',
            'ocr_color': '',
            'ocr_box': '',
            'render': 'false',
        }

        st = time.time()
        print("开始发送请求到远程识别服务...")
        response = requests.post("http://ai.bygpu.com:58118/ocr", data=data, files=files)
        print(f"请求完成，耗时：{time.time() - st:.2f}s")

    # 解析返回内容
    try:
        result = response.json()
    except Exception as e:
        print(f"JSON解析失败: {e}")
        return

    # 保存返回 JSON（调试用）
    json_path = os.path.join(res_path, 'test.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 提取 kern 内容
    if isinstance(result, dict) and 'result' in result:
        kern_data = result['result']
    elif isinstance(result, str):
        kern_data = result
    else:
        print("返回格式不正确，未找到有效 kern 数据")
        return

    # 保存为 .krn 文件
    kern_path = os.path.join(res_path, 'result.krn')
    with open(kern_path, 'w', encoding='utf-8') as f:
        f.write(kern_data)
    print(f"krn 文件已保存: {kern_path}")

    # 生成 MIDI 文件
    try:
        score = converter.parse(kern_data)
        midi_path = os.path.join(res_path, 'temp.mid')
        score.write('midi', fp=midi_path)
        print(f"MIDI 文件已生成: {midi_path}")
    except Exception as e:
        print(f"生成 MIDI 失败: {e}")
