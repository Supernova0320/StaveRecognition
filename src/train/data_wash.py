import os


def clean_krn_file(input_path, output_path):
    """清除以 '!!!' 或 '!!' 开头的注释行，并保存到新文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = [line for line in lines if not line.strip().startswith('!!')]

    # 创建输出目录（如果不存在）
    os.makedirs(output_path, exist_ok=True)
    output_file_path = os.path.join(output_path, os.path.basename(input_path))

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    print(f"[✓] 清洗完成: {output_file_path}")


def clean_all_krn_files_in_dir(label_dir, output_dir):
    """批量清洗目录中所有 .krn 文件的注释行，并保留原始文件"""
    for filename in os.listdir(label_dir):
        if filename.lower().endswith('.krn'):
            filepath = os.path.join(label_dir, filename)
            clean_krn_file(filepath, output_dir)


if __name__ == '__main__':
    label_dir = r'F:\Graduation Design\Dataset\new\labels'  # 输入文件目录
    output_dir = r'F:\Graduation Design\Dataset\new\labels'  # 输出目录

    clean_all_krn_files_in_dir(label_dir, output_dir)
