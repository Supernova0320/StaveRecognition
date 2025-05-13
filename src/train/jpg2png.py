from PIL import Image
import os

# 获取当前目录下的所有文件
input_directory = r'F:\Graduation Design\Dataset\grandstaff\images'  # 你可以根据需要修改这个路径
output_directory = r'F:\Graduation Design\Dataset\grandstaff\images'  # 输出的PNG文件夹

# 如果输出目录不存在，创建它
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 遍历当前目录下的所有文件
for filename in os.listdir(input_directory):
    if filename.lower().endswith('.jpg'):
        # 打开JPG图片
        img_path = os.path.join(input_directory, filename)
        img = Image.open(img_path)

        # 构造PNG文件的路径
        new_filename = os.path.splitext(filename)[0] + '.png'
        output_path = os.path.join(output_directory, new_filename)

        # 保存为PNG格式
        img.save(output_path, 'PNG')
        print(f"已转换: {filename} -> {new_filename}")

print("所有转换已完成。")
