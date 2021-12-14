from utils.get_md5_data import get_md5_pwd

if __name__ == '__main__':
    pwd = "123456"
    md5_pwd = get_md5_pwd(pwd)
    print(md5_pwd)
