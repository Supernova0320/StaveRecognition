import os
import json


class GrandStaffDatasetBuilder:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def read_file_auto_encoding(self, filepath):
        """自动尝试多种编码读取文件"""
        encodings_to_try = ['utf-8', 'utf-8-sig', 'gbk', 'iso-8859-1']
        for enc in encodings_to_try:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(f"❌ 无法解码文件：{filepath}，请检查编码格式")

    def generate_data(self, image_path, label_path):
        save_list = []

        for file in os.listdir(label_path):
            if not file.lower().endswith('.krn'):
                continue

            base_name = os.path.splitext(file)[0]
            krn_path = os.path.join(label_path, file)

            try:
                # 使用自动编码识别的函数读取文件内容
                krn_text = self.read_file_auto_encoding(krn_path).strip()
            except UnicodeDecodeError as e:
                print(f"[错误] 无法读取标签文件: {krn_path}")
                print(f"详细信息: {e}")
                continue

            if not krn_text:
                print(f"[跳过] 空标签文件: {krn_path}")
                continue

            # 可能存在的两张图片
            for suffix in ['', '_distortion']:
                image_file = f"{base_name}{suffix}.png"
                image_full_path = os.path.join(image_path, image_file)

                if os.path.exists(image_full_path):
                    data_entry = {
                        "image": f"images/{image_file}",
                        "conversations": [
                            {"from": "human", "value": "<image>\nOCR:"},
                            {"from": "gpt", "value": krn_text}
                        ]
                    }
                    save_list.append(data_entry)
                    print(f"[✓] 加入图像: {image_file}")
                else:
                    print(f"[⚠] 缺失图像: {image_file}")

        # 写入最终 JSON 文件
        output_path = os.path.join(self.dataset_path, 'data.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(save_list, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 数据集构建完成，样本总数：{len(save_list)}")
        print(f"✅ 保存路径：{output_path}")


if __name__ == '__main__':
    image_path = r'F:\Graduation Design\Dataset\new\images'
    label_path = r'F:\Graduation Design\Dataset\new\labels'
    dataset_path = r'F:\Graduation Design\Dataset\new'

    builder = GrandStaffDatasetBuilder(dataset_path)
    builder.generate_data(image_path, label_path)
