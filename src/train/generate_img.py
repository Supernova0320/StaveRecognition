import verovio
import os
from pathlib import Path
import random


# 在 SVG 中注入白色背景矩形
def inject_white_background(svg_content):
    insert_pos = svg_content.find('>') + 1
    rect = '<rect width="100%" height="100%" fill="white"/>'
    return svg_content[:insert_pos] + rect + svg_content[insert_pos:]


# 处理单个 krn 文件，输出白底 SVG
def generate_svg_from_krn(krn_file, output_dir):
    try:
        with open(krn_file, 'r', encoding='utf-8') as f:
            kern_data = f.read()
    except UnicodeDecodeError:
        print(f"文件 {krn_file} 编码错误，已删除并跳过。")
        os.remove(krn_file)
        return

    page_width = random.randint(1800, 2400)

    tk = verovio.toolkit()
    tk.setOptions({
        "scale": 40,
        "adjustPageHeight": True,
        "pageWidth": page_width,  # 随机宽度
        "pageHeight": 60000,
        "footer": "none"
    })
    tk.loadData(kern_data)

    # 自动高度下只生成一页
    svg = tk.renderToSVG(1)
    svg = inject_white_background(svg)

    svg_file = os.path.join(output_dir, f"{Path(krn_file).stem}.svg")
    with open(svg_file, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"已输出 SVG（白底，宽度 {page_width}，高度自适应）：{svg_file}")


# 批量处理 krn 文件夹
def batch_process_krn_to_svg(input_dir, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for krn_file in Path(input_dir).rglob('*.krn'):
        print(f"正在处理：{krn_file}")
        generate_svg_from_krn(krn_file, output_dir)


# 设置路径
input_dir = r'F:\Graduation Design\StaveRecognition\midi_file'
output_dir = r'F:\Graduation Design\StaveRecognition\midi_file'

# 执行批量转换
batch_process_krn_to_svg(input_dir, output_dir)
