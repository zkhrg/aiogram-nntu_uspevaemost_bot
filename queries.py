import sqlite3 as sq
import parse


class DataBase:

    def __init__(self):
        with sq.connect("BOT_v1.db") as self.con:
            self.cur = self.con.cursor()

    def checkChatId(self, chat_id):
        self.cur.execute("DELETE FROM users WHERE chat_id == ''")
        self.con.commit()
        self.cur.execute(f"SELECT chat_id FROM users WHERE chat_id == {chat_id}")
        result = self.cur.fetchall()
        if not result:
            return False
        else:
            return True

    def addChatId(self, chat_id):
        self.cur.execute(f"INSERT INTO users(chat_id) VALUES({chat_id})")
        self.con.commit()
        self.cur.execute(f"SELECT chat_id FROM users WHERE chat_id == {chat_id}")
        result = self.cur.fetchall()
        print(result[0][0])

    def changeValue(self, to_change, something, chat_id):
        self.cur.execute(f"UPDATE users SET {to_change} = '{something}' WHERE chat_id == {chat_id}")
        self.con.commit()

    def findData(self, chat_id):
        self.cur.execute(f"SELECT * FROM users WHERE chat_id == {chat_id}")
        result = self.cur.fetchall()
        r1 = parse.post_request(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])

        return r1

    def actualInfo(self, chat_id):
        self.cur.execute(f"SELECT * FROM users WHERE chat_id == {chat_id}")
        result = self.cur.fetchall()
        if result[0][5] == "bak_spec":
            l_type = "Бакалавриат/Специалитет"
        elif result[0][5] == "mag":
            l_type = "Магистратура"
        else:
            l_type = ''
        act_info = f"<b>Имя:</b> {result[0][1]}\n" \
                  f"<b>Фамилия:</b> {result[0][2]}\n" \
                  f"<b>Отчество:</b> {result[0][3]}\n" \
                  f"<b>Номер студенческого:</b> {result[0][4]}\n" \
                  f"<b>Тип обучения:</b> {l_type}"
        return act_info

    def parseDB(self):
        self.cur.execute(f"SELECT * FROM users")
        result = self.cur.fetchall()
        string_result = '<code>'
        for i in range(len(result)):
            for j in range(6):
                string_result += f'{result[i][j]}'
            string_result += f'\n\n'

        return string_result+'</code>'


db = DataBase()
