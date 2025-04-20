# 客户端
import base64
import time
import requests

from music21 import converter


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def run_recognition(image_path):
    res_path = r'F:/Graduation Design/StaveRecognition/midi_file/'
    base64_image = image_to_base64(image_path)
    data = {
        "image": f"{base64_image}",
        "ocr_type": "format",
        "ocr_color": '',
        "ocr_box": '',
        "render": True,  # 生成渲染后的html
        "save_render_file": res_path + 'res1.html'
    }
    st = time.time()
    print("开始请求···")
    response = requests.post("http://localhost:8848/ocr", json=data)
    print(f"已完成，请求耗时：{time.time() - st}s")

    # 将kern转为Midi
    kern_score = response.json()
    score = converter.parse(kern_score)

    midi_path = res_path + 'temp.mid'
    score.write('midi', fp=midi_path)
    print("已生成midi文件")
