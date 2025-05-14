import os


def levenshtein_distance(s1, s2):
    """计算Levenshtein距离"""
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + 1
                )
    return dp[len_s1][len_s2]


def token_accuracy(ref_text, pred_text):
    """基于Kern语法的Token级精度评估"""
    ref_tokens = ref_text.strip().split()
    pred_tokens = pred_text.strip().split()

    min_len = min(len(ref_tokens), len(pred_tokens))
    match_count = sum(1 for i in range(min_len) if ref_tokens[i] == pred_tokens[i])
    return match_count / len(ref_tokens) if ref_tokens else 0.0


def evaluate_krn(ref_text, pred_text):
    """计算一对文件的评估值"""
    ld = levenshtein_distance(ref_text, pred_text)
    norm_ld = ld / max(1, len(ref_text))
    token_acc = token_accuracy(ref_text, pred_text)
    return norm_ld, token_acc


def batch_evaluate_krn(ref_dir, pred_dir):
    """批量评估两个目录下的所有 .krn 文件"""
    total_ld = 0.0
    total_acc = 0.0
    count = 0

    print("=== 批量 Kern 乐谱识别评估结果 ===")

    for filename in os.listdir(ref_dir):
        if filename.endswith(".krn"):
            ref_path = os.path.join(ref_dir, filename)
            pred_path = os.path.join(pred_dir, filename)

            if not os.path.exists(pred_path):
                print(f"[跳过] 缺少预测文件: {filename}")
                continue

            with open(ref_path, 'r', encoding='utf-8') as f1, open(pred_path, 'r', encoding='utf-8') as f2:
                ref_text = f1.read()
                pred_text = f2.read()

            norm_ld, token_acc = evaluate_krn(ref_text, pred_text)

            print(f"\n文件: {filename}")
            print(f"  - 归一化编辑距离 (LD): {norm_ld:.4f}")
            print(f"  - Token级准确率     : {token_acc:.4f}")

            total_ld += norm_ld
            total_acc += token_acc
            count += 1

    # 输出平均值
    if count > 0:
        avg_ld = total_ld / count
        avg_acc = total_acc / count
        print("\n=== 总体评估 ===")
        print(f"平均归一化编辑距离 (LD): {avg_ld:.4f}")
        print(f"平均Token级准确率     : {avg_acc:.4f}")
    else:
        print("未找到可评估的 .krn 文件对。")


if __name__ == "__main__":
    # 替换为你的标签目录和预测目录路径
    reference_dir = r"F:\Graduation Design\Dataset\test_normal\labels"
    prediction_dir = r"F:\Graduation Design\Dataset\test_normal\res_labels"

    batch_evaluate_krn(reference_dir, prediction_dir)