# 客户端
import time
import requests

from music21 import converter


def run_recognition(image_path):
    res_path = r'F:/Graduation Design/StaveRecognition/midi_file/'
    data = {
        "image_path": image_path,  # 改成传路径
        "ocr_type": "format",
        "ocr_color": '',
        "ocr_box": '',
        "render": True,
        "save_render_file": res_path + 'res1.html'
    }

    st = time.time()
    print("开始请求···")
    response = requests.post("http://localhost:8848/ocr", json=data)
    print(f"已完成，请求耗时：{time.time() - st}s")

    kern_score = response.json()
    score = converter.parse(kern_score)

    midi_path = res_path + 'temp.mid'
    score.write('midi', fp=midi_path)
    print("已生成midi文件")

