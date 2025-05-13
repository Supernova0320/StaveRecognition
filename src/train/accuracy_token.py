def tokenize_kern(kern_text):
    """
    将Kern乐谱文本按空格和换行符拆分为原子化的符号单元（token）。
    """
    # 按空格和换行符分隔符号
    tokens = kern_text.replace("\n", " ").split()
    return tokens


def compute_symbol_accuracy(pred_kern, gt_kern):
    """
    计算预测的kern与标注kern的符号级准确率（token级比对）。
    """
    pred_tokens = tokenize_kern(pred_kern)
    gt_tokens = tokenize_kern(gt_kern)

    # 符号总数
    total_tokens = len(gt_tokens)

    if total_tokens == 0:
        return 100.0  # 如果没有任何符号，则认为完全匹配

    # 统计匹配的符号数量
    matched_tokens = sum(1 for p, g in zip(pred_tokens, gt_tokens) if p == g)

    # 计算准确率
    accuracy = (matched_tokens / total_tokens) * 100
    return accuracy


# 读取文件内容
def read_kern_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# 示例用法
pred_kern_file = r"F:\Graduation Design\StaveRecognition\midi_file\result.krn"  # 识别后的文件
gt_kern_file = r"F:\Graduation Design\StaveRecognition\midi_file\test.krn"  # 标注的正确文件

# 读取kern文本
pred_kern = read_kern_file(pred_kern_file)
gt_kern = read_kern_file(gt_kern_file)

# 计算符号级准确率
accuracy = compute_symbol_accuracy(pred_kern, gt_kern)
print(f"符号级准确率：{accuracy:.2f}%")
