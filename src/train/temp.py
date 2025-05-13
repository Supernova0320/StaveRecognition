import os
from PIL import Image


def delete_large_pngs_and_krns(png_directory, krn_directory):
    for filename in os.listdir(png_directory):
        file_path_png = os.path.join(png_directory, filename)

        if filename.lower().endswith('.png'):
            try:
                with Image.open(file_path_png) as img:
                    img.load()  # 强制读取图像数据
                    width, height = img.size

                if height > 1000:
                    # 删除PNG文件
                    os.remove(file_path_png)
                    print(f"已删除：{file_path_png}")

                    # 查找并删除同名的 .krn 文件
                    krn_filename = filename.replace('.png', '.krn')
                    file_path_krn = os.path.join(krn_directory, krn_filename)

                    # 如果 .krn 文件存在，删除该文件
                    if os.path.exists(file_path_krn):
                        os.remove(file_path_krn)
                        print(f"已删除同名 krn 文件：{file_path_krn}")
                    else:
                        print(f"未找到同名 .krn 文件，跳过删除：{file_path_krn}")

            except Exception as e:
                print(f"无法处理文件 {file_path_png}: {e}")


# 设置目录路径
png_directory = r'F:\Graduation Design\Dataset\dual\images'
krn_directory = r'F:\Graduation Design\Dataset\dual\labels'

delete_large_pngs_and_krns(png_directory, krn_directory)
