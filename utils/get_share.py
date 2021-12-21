import random


# 生成n位长度的字符串
def get_share_random_str(n: int):
    s_list = []
    for i in range(n):
        s = random.choice("abcdefghijklmnopqrstuvwxyz"
                          "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                          "0123456789")
        s_list.append(s)

    return "".join(s_list)


if __name__ == '__main__':
    a = get_share_random_str(16)
    print(a)
