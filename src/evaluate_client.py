import time
import requests
import os


def run_recognition(image_path):
    """
    输入本地 PNG 图片路径，发送到远程服务识别五线谱，并保存为同名的 .krn 文件。
    """
    res_path = r'F:\Graduation Design\Dataset\test_normal\res_labels'
    os.makedirs(res_path, exist_ok=True)

    image_name = os.path.splitext(os.path.basename(image_path))[0]  # 提取文件名（无扩展名）

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
        print(f"开始识别: {image_name}")
        response = requests.post("http://ai.bygpu.com:58118/ocr", data=data, files=files)
        print(f"识别完成，耗时：{time.time() - st:.2f}s")

    # 解析返回 JSON 内容
    try:
        result = response.json()
    except Exception as e:
        print(f"JSON 解析失败: {e}")
        return

    # 提取 kern 内容并保存
    kern_data = result.get("result", "")
    if not kern_data:
        print("未找到有效的 kern 数据")
        return

    kern_path = os.path.join(res_path, f'{image_name}.krn')
    with open(kern_path, 'w', encoding='utf-8') as f:
        f.write(kern_data)
    print(f"krn 文件已保存: {kern_path}")
