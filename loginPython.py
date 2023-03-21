loggedUsrIndex = None
db = []


def login_main():
    global loggedUsrIndex
    option = int(input("enter option:\n"
                       "1. login\n"
                       "2. sign up\n"
                       "3. exit\n"))
    match option:
        case 1:
            login()
            if loggedUsrIndex is not None:
                login_second()
            else:
                login_main()
        case 2:
            sign_up()
            login_main()
        case _:
            exit(0)


def login():
    global db
    global loggedUsrIndex
    username = input("Enter username:")
    password = input("Enter password:")
    uid = get_uid(username)
    if uid is not None:
        if db[uid]["password"] == password:
            loggedUsrIndex = uid
            print("logged in!")
        else:
            print("wrong password!")
            login()
    else:
        print("failed!")


def get_uid(username):
    global db
    for i in range(len(db)):
        if db[i]["username"] == username:
            return i
    return None


def sign_up():
    usr_dict = {}
    username = get_username()
    if get_uid(username) is None:
        usr_dict.update({"username": username})
        name = input("Enter private name: ")
        usr_dict.update({"private": name})
        family = input("Enter family name: ")
        usr_dict.update({"family": family})
        add_passwd(usr_dict)
        add_mail(usr_dict)
        add_phone(usr_dict)
        add_gender(usr_dict)
        is_admin = bool(int(input("Are you admin(1/0): ")))
        usr_dict.update({"isAdmin": is_admin})
        db.append(usr_dict)
    else:
        print("username exists!")


def get_username():
    username = input("Enter username: ")
    if username == "":
        get_username()
    else:
        return username


def add_passwd(usr_dict):
    passwd = input("Enter password: ")
    if len(passwd) > 8:
        usr_dict.update({"password": passwd})
    else:
        print("please enter more then 8 characters")
        add_passwd(usr_dict)


def add_mail(usr_dict):
    mail = input("Enter email: ")
    if "@" in mail:
        usr_dict.update({"email": mail})
    else:
        print("please use @ in your mail!")
        add_mail(usr_dict)


def add_phone(usr_dict):
    phone = input("Enter phone number: ")
    if phone.isnumeric():
        usr_dict.update({"phone": phone})
    else:
        print("not a number!")
        add_phone(usr_dict)


def add_gender(usr_dict):
    sex = input("Enter gender(male/female): ")
    if sex != "male" and sex != "female":
        print("please enter male or female!")
        add_gender(usr_dict)
    else:
        usr_dict.update({"gender": sex})


def login_second():
    global loggedUsrIndex
    option = int(input("Logged on!\n"
                       "Enter option:\n"
                       "1. del user (admins only)\n"
                       "2. edit user (admins only)\n"
                       "3.show all users\n"
                       "4. exit\n"))
    match option:
        case 1:
            if is_usr_admin():
                username = input("Enter username to delete: ")
                del_user(username)
        case 2:
            if is_usr_admin():
                edit_user()
        case 3:
            show_all()
        case _:
            loggedUsrIndex = None
            login_main()
    login_second()


def is_usr_admin():
    global db
    global loggedUsrIndex
    is_admin = db[loggedUsrIndex]["isAdmin"]
    if not is_admin:
        print("You are not an admin!")
    return is_admin


def del_user(username):
    global db
    global loggedUsrIndex
    uid = get_uid(username)
    if uid is None:
        print("no such user!")
    else:
        if uid == loggedUsrIndex:
            loggedUsrIndex = None
            db.pop(uid)
            print("deleted yourself!")
            login_main()
        else:
            db.pop(uid)


def edit_user():
    global loggedUsrIndex
    uid = get_uid(input("enter username of the user you wish to edit:"))
    if uid is not loggedUsrIndex:
        del_user(db[uid]["username"])
        sign_up()
    else:
        print("can't edit logged on user!")


def show_all():
    global db
    for i in db:
        print(f"user {db.index(i) + 1}:")
        for key, val in i.items():
            print(f"    {key}: {val}")


login_main()
