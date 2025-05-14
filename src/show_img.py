import verovio
from pathlib import Path


# 在 SVG 中注入白色背景矩形
def inject_white_background(svg_content):
    insert_pos = svg_content.find('>') + 1
    rect = '<rect width="100%" height="100%" fill="white"/>'
    return svg_content[:insert_pos] + rect + svg_content[insert_pos:]


# 处理固定路径 input_dir/result.krn，并输出 result.svg
def generate_svg(input_dir):
    input_dir = Path(input_dir)
    krn_file = input_dir / "result.krn"
    svg_file = input_dir / "result.svg"

    if not krn_file.exists():
        print(f"未找到 krn 文件: {krn_file}")
        return

    with open(krn_file, 'r', encoding='utf-8') as f:
        kern_data = f.read()

    tk = verovio.toolkit()
    tk.setOptions({
        "scale": 40,
        "adjustPageHeight": True,
        "pageWidth": 650,
        "pageHeight": 800,
        "footer": "none"
    })
    tk.loadData(kern_data)

    # 渲染第一页
    svg = tk.renderToSVG(1)
    svg = inject_white_background(svg)

    with open(svg_file, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"已生成 SVG 文件")


generate_svg(r"F:\Graduation Design\StaveRecognition\midi_file")
