import time
import requests
import os
from music21 import converter


def run_recognition(image_path):
    """
    输入本地 PNG 图片路径，发送到远程服务识别五线谱，生成 krn、midi 和 html 文件。
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
            'render': 'true',
        }

        st = time.time()
        print("开始发送请求到远程识别服务...")
        response = requests.post("http://ai.bygpu.com:58118/ocr", data=data, files=files)
        print(f"请求完成，耗时：{time.time() - st:.2f}s")

    # 解析返回 JSON 内容
    try:
        result = response.json()
    except Exception as e:
        print(f"JSON解析失败: {e}")
        return

    # 提取 kern 内容
    kern_data = result.get("result", "")
    if not kern_data:
        print("未找到有效的 kern 数据")
        return

    # 保存 .krn 文件
    kern_path = os.path.join(res_path, 'result.krn')
    with open(kern_path, 'w', encoding='utf-8') as f:
        f.write(kern_data)
    print(f"krn 文件已保存: {kern_path}")

    # 保存 html 文件
    html_content = result.get("html", "")
    if html_content.strip():
        html_path = os.path.join(res_path, 'result.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML 文件已保存: {html_path}")
    else:
        print("返回中未包含 HTML 内容")

    # 使用 music21 转换生成 MIDI
    try:
        score = converter.parse(kern_data)
        midi_path = os.path.join(res_path, 'temp.mid')
        score.write('midi', fp=midi_path)
        print(f"MIDI 文件已生成: {midi_path}")
    except Exception as e:
        print(f"生成 MIDI 失败: {e}")
