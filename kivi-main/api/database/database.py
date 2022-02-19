import sqlite3
from sqlite3.dbapi2 import Cursor


class DataCrude():
    def __init__(self) -> None:
        self.sqlconn = sqlite3.connect(
            "databasename.db", check_same_thread=False)
        self.fether = self.sqlconn.cursor()
        self.usersname = []
        self.password = []
        self.utr = []
        self.money = []
        self.users = {}
        self.DoDIctUsers()

    def seckeyget(self):

        self.fether.execute(
            f"SELECT key FROM Key;")
        key = self.fether.fetchall()
        return key[0][0]

    def PostMoney(self, myname, name, moneyvalue, value):
        value = int(value)
        if self.CheakMoney(myname, moneyvalue, value) == True:
            self.fether.execute(
                f"UPDATE Users Set {moneyvalue} = {moneyvalue} + {value} WHERE name = '{name}'")
            self.sqlconn.commit()
            self.fether.execute(
                f"UPDATE Users Set {moneyvalue} = {moneyvalue} - {value} WHERE name = '{myname}'")
            self.sqlconn.commit()
            return True
        else:
            return False

    def CheakMoney(self, name, moneyvalue, value):
        self.fether.execute(
            f"SELECT USD, UAH, RUB FROM Users WHERE name = '{name}'")
        info = self.fether.fetchall()
        infomoney = {f"{name}": {
            "USD": info[0][0],
            "UAH": info[0][1],
            "RUB": info[0][2]
        }}

        if infomoney.get(f"{name}").get(f"{moneyvalue}") >= value:

            return True
        else:
            return False

    def RecordAllName(self):
        self.usersname = []

        self.fether.execute("SELECT name, password FROM Users;")
        record = self.fether.fetchall()

        for i in range(len(record)):
            self.usersname.append(record[i][0])

    def PrintUserToBase(self, name, password):
        self.fether.execute(
            f"INSERT INTO Users (name, password) VALUES ('{name}', '{password}');")
        self.sqlconn.commit()

    def RecordAllPasswords(self):
        self.password = []

        for i in range(len(self.usersname)):
            self.fether.execute(
                f"SELECT password FROM Users Where name = '{self.usersname[i]}';")
            record = self.fether.fetchall()
            for i in range(len(record)):
                self.password.append(record[i][0])

    def DoDIctUsers(self):
        self.RecordAllName()
        self.RecordAllPasswords()
        self.users = {}

        for i in range(len(self.usersname)):

            self.fether.execute(
                f"SELECT USD, UAH, RUB FROM Users WHERE name = '{self.usersname[i]}'")
            info = self.fether.fetchall()
            infomoney = {
                "USD": info[0][0],
                "UAH": info[0][1],
                "RUB": info[0][2]
            }

            self.utr.append(
                [str(self.usersname[i]), {"password": str(self.password[i]), "money": infomoney}])
            self.utr = dict(self.utr)
            self.users.update(self.utr)
            self.utr = []

    def ConnClose(self):
        self.sqlconn.close()


b = DataCrude()
b.DoDIctUsers()
