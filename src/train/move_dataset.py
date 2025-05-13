import os
import shutil

# 设置根目录路径（这里是当前目录）
root_dir = r'F:\Graduation Design\Dataset\new'
# 设置目标文件夹
target_dir = os.path.join(root_dir, 'labels')

# 创建目标文件夹（如果不存在）
os.makedirs(target_dir, exist_ok=True)

# 遍历根目录下的所有子文件夹
for folder_name in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder_name)

    # 只处理文件夹
    if os.path.isdir(folder_path) and folder_name != 'labels':
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.krn'):
                old_file_path = os.path.join(folder_path, file_name)
                new_file_name = f"{folder_name}_{file_name}"
                new_file_path = os.path.join(target_dir, new_file_name)

                # 移动并重命名文件
                shutil.move(old_file_path, new_file_path)

print("所有 .krn 文件已重命名并移动到 labels 文件夹中。")
