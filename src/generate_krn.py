import os
from evaluate_client import run_recognition  # 替换为你的模块文件名，例如 from client import run_recognition


def batch_process_pngs(image_dir):
    """
    批量处理目录下所有 PNG 文件，调用远程识别服务并保存结果。
    """
    if not os.path.isdir(image_dir):
        print(f"目录不存在: {image_dir}")
        return

    # 遍历所有 PNG 文件
    for filename in os.listdir(image_dir):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(image_dir, filename)
            print(f"\n正在处理文件: {image_path}")
            try:
                run_recognition(image_path)
            except Exception as e:
                print(f"处理 {filename} 时发生错误: {e}")


if __name__ == '__main__':
    # 修改为你想要处理的 PNG 图片所在的目录
    png_folder = r'F:\Graduation Design\Dataset\test_normal\images'
    batch_process_pngs(png_folder)
