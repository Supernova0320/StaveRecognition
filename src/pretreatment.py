import mido


def get_future_part(p_mid, i, target_time):
    future_part = []
    index = i
    while p_mid[index]:
        if p_mid[index]["start_time"] > p_mid[i]["start_time"] + target_time:
            break
        future_part.append(p_mid[index])
        index += 1
    return future_part


def cal_note_length(partition):
    """
    计算每个音符开始播放的绝对时间，并根据velocity映射到音符长度
    """
    i = 0
    while partition[i]:
        if partition[i]["msg"].type == "note_on" and partition[i]["msg"].velocity > 0:  # 是正在播放的音符
            start_time = partition[i]["start_time"]
            duration = partition[i]["msg"].velocity / 10
            forward = i + 1
            while partition[forward]:  # 遍历i之后，截止时间之前的每一个事件
                if partition[forward]["start_time"] + 0.05 > start_time + duration:
                    break
                msg = partition[forward]["msg"]

                # 要么note_off要么note_on且velocity == 0
                if msg.type in ["note_on", "note_off"]:
                    if msg.note == partition[i]["msg"].note:
                        note_length = partition[forward]["start_time"] - start_time - 0.05
                        partition[i]["note_length"] = note_length
                        break
                forward += 1
        i += 1
    return partition


def treat(mid):
    abs_time = 1
    partition = []
    # 把相对时间delta time变成绝对时间
    for msg in mid:
        abs_time += msg.time
        if isinstance(msg, mido.MetaMessage):
            continue
        partition.append(
            {"start_time": abs_time, "msg": msg, "note_length": 0}
        )
    partition.append(None)
    partition = cal_note_length(partition)
    length = partition[-2]["start_time"]
    return partition, length
