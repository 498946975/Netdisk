import os


def create_dir(dir: str):
    is_exist = os.path.exists(dir)

    if not is_exist:
        os.mkdir(dir)  # 创建一级
        # os.makedirs() # 创建多级
        return True
    else:
        return False
