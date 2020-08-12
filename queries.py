import sqlite3 as sq
import parse

with sq.connect("BOT_v1.db") as con:
    cur = con.cursor()


def checkChatId(chat_id):
    cur.execute("DELETE FROM users WHERE chat_id == ''")
    con.commit()
    cur.execute(f"SELECT chat_id FROM users WHERE chat_id == {chat_id}")
    result = cur.fetchall()
    if not result:
        return False
    else:
        return True


def addChatId(chat_id):
    cur.execute(f"INSERT INTO users(chat_id) VALUES({chat_id})")
    con.commit()
    cur.execute(f"SELECT chat_id FROM users WHERE chat_id == {chat_id}")
    result = cur.fetchall()
    print(result[0][0])


def changeName(name, chat_id):
    cur.execute(f"UPDATE users SET name = '{name}' WHERE chat_id == {chat_id}")
    con.commit()


def changeSurname(surname, chat_id):
    cur.execute(f"UPDATE users SET surname = '{surname}' WHERE chat_id == {chat_id}")
    con.commit()


def changeFathername(fathername, chat_id):
    cur.execute(f"UPDATE users SET fathername = '{fathername}' WHERE chat_id == {chat_id}")
    con.commit()


def changeNZach(n_zach, chat_id):
    cur.execute(f"UPDATE users SET n_zach = '{n_zach}' WHERE chat_id == {chat_id}")
    con.commit()


def changeLearnType(learn_type, chat_id):
    cur.execute(f"UPDATE users SET learn_type = '{learn_type}' WHERE chat_id == {chat_id}")
    con.commit()


def findData(chat_id):
    cur.execute(f"SELECT * FROM users WHERE chat_id == {chat_id}")
    result = cur.fetchall()
    r1 = parse.post_request(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])

    return r1


def actualInfo(chat_id):
    cur.execute(f"SELECT * FROM users WHERE chat_id == {chat_id}")
    result = cur.fetchall()
    l_type = ''
    if result[0][5] == "bak_spec":
        l_type = "Бакалавриат/Специалитет"
    elif result[0][5] == "mag":
        l_type = "Магистратура"
    else:
        l_type = ''
    actInfo = f"<b>Имя:</b> {result[0][1]}\n" \
              f"<b>Фамилия:</b> {result[0][2]}\n" \
              f"<b>Отчество:</b> {result[0][3]}\n" \
              f"<b>Номер студенческого:</b> {result[0][4]}\n" \
              f"<b>Тип обучения:</b> {l_type}"
    return actInfo
