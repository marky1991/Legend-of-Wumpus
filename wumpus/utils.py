def get_git_password():
    password_file = open("../../passwords.txt", "r")
    password = password_file.readlines()[0].strip()
    password_file.close()
    return password
