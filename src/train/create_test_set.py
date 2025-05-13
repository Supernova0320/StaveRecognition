import os
import random
import shutil


def split_dataset(dataset_dir, test_size=0.2):
    # 设置路径
    images_dir = os.path.join(dataset_dir, 'images')
    labels_dir = os.path.join(dataset_dir, 'labels')

    # 创建测试集目录
    test_images_dir = os.path.join(dataset_dir, 'test', 'images')
    test_labels_dir = os.path.join(dataset_dir, 'test', 'labels')

    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_labels_dir, exist_ok=True)

    # 获取所有图像文件
    image_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]

    # 随机选取 test_size 的比例作为测试集
    test_files = random.sample(image_files, int(len(image_files) * test_size))

    # 拷贝测试集文件到测试集目录
    for image_file in test_files:
        # 去掉 _distorted 后缀来找到对应的标签文件
        base_name = image_file.replace('_distorted.png', '.png')
        label_file = base_name.replace('.png', '.krn')

        image_path = os.path.join(images_dir, image_file)
        label_path = os.path.join(labels_dir, label_file)

        if os.path.exists(label_path):  # 确保标签文件存在
            # 拷贝到新的测试集目录
            shutil.copy(image_path, os.path.join(test_images_dir, image_file))
            shutil.copy(label_path, os.path.join(test_labels_dir, label_file))
            print(f"已拷贝测试集：{image_file} 和 {label_file}")

            # 删除原始文件
            os.remove(image_path)
            os.remove(label_path)
            print(f"已删除文件：{image_file} 和 {label_file}")
        else:
            print(f"警告：未找到标签文件 {label_file}，跳过 {image_file}")


# 设置数据集目录路径
dataset_dir = r'F:\Graduation Design\Dataset\grandstaff'

# 调用函数，随机提取20%的测试集
split_dataset(dataset_dir, test_size=0.2)
