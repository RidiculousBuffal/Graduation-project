from werkzeug.security import check_password_hash

if __name__ == '__main__':
    password = "Zhougezuishuai22"

    # 生成哈希值
    hashed_pass = 'scrypt:32768:8:1$69FKq75dbz3Gop6o$ee394793186321c7e16731796d9737c6a8f0d7c47e3ac92d0da3f98ab8abe9d35585881bee07bdc41743ff385e6d2b6accb9db221a9a2450a21b9347df208bab'

    # 校验密码
    is_valid = check_password_hash(hashed_pass, password)

    print(f"Hashed Password: {hashed_pass}")
    print(f"Password is valid: {is_valid}")
