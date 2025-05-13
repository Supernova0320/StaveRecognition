import Levenshtein


def is_music_data(line: str) -> bool:
    """判断是否为音乐数据行（排除元信息）"""
    return not line.startswith("*") and not line.startswith("**") and line.strip() != "="


def calculate_file_accuracy(pred_lines, gt_lines):
    total_distance = 0
    total_length = 0
    line_count = 0

    for pred_line, gt_line in zip(pred_lines, gt_lines):
        # 拆分每个声部（按tab或空格）
        pred_fields = pred_line.strip().split()
        gt_fields = gt_line.strip().split()

        # 跳过元信息行
        if not is_music_data(pred_line):
            continue

        for pred, gt in zip(pred_fields, gt_fields):
            distance = Levenshtein.distance(pred, gt)
            max_len = max(len(pred), len(gt))
            total_distance += distance
            total_length += max_len
            line_count += 1

    if total_length == 0:
        return 100.0

    accuracy = (1 - total_distance / total_length) * 100
    return accuracy


# 读取两个文件
with open(r"F:\Graduation Design\StaveRecognition\midi_file\result.krn", "r", encoding="utf-8") as f1, open(
        r"F:\Graduation Design\StaveRecognition\midi_file\test.krn", "r", encoding="utf-8") as f2:
    pred_lines = f1.readlines()
    gt_lines = f2.readlines()

# 计算准确度
accuracy = calculate_file_accuracy(pred_lines, gt_lines)
print(f"整体识别准确度：{accuracy:.2f}%")
