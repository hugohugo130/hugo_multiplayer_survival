import threading
from time import time as getts
import hashlib
from time import sleep as slp

try:
    import mysql.connector as mysql
    from mysql.connector import Error
    from tkinter import messagebox
except ModuleNotFoundError:
    from subprocess import run
    from sys import executable

    run(
        [
            executable,
            "-m",
            "pip",
            "install",
            "mysql-connector-python",
        ]
    )
    import mysql.connector as mysql
    from mysql.connector import Error


def hash_password(password) -> str:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    sha512_hash = hashlib.sha512()
    sha512_hash.update(password.encode("utf-8"))
    return sha512_hash.hexdigest()


def is_sha512_hash(hash_string: str) -> bool:
    if len(hash_string) != 128:
        return False

    try:
        int(hash_string, 16)
        return True
    except ValueError:
        return False


def get_player_data_tuple(
    addhpcache,
    coinlvl,
    healthlvl,
    swordlvl,
    coins,
    cu,
    cuosf,
    darkmode,
    darkmodecolor,
    difficult,
    hp,
    langchoose,
    monsternum,
    password,
    playername,
    food,
    hunger,
    tick,
    online,
):
    if not is_sha512_hash(password):
        password = hash_password(password)

    return (
        addhpcache,
        coinlvl,
        healthlvl,
        swordlvl,
        coins,
        cu,
        cuosf,
        darkmode,
        darkmodecolor,
        difficult,
        hp,
        langchoose,
        monsternum,
        password,
        playername,
        food,
        hunger,
        tick,
        online,
    )


class DatabaseModule:
    def __init__(self):
        self.hostname = "i4q.h.filess.io"
        self.database = "SurvivalGameDatabase_waveleast"
        self.port = "3307"
        self.username = "SurvivalGameDatabase_waveleast"
        self.loginpassword = "26c2e76ce7825addd2ef214dd23636b04d375a3a"
        # =================================
        # self.hostname = "fdb1029.awardspace.net"
        # self.database = "4607383_multiplayersurvival"
        # self.port = "3306"
        # self.username = "4607383_multiplayersurvival"
        # self.loginpassword = "26c2e76ce7825addd2ef214dd23636b04d375a3a"
        # =================================
        self.database_table_name = "players"
        self.db = None
        self.cursor = None
        self.retry_count = 0

    def connect(self):
        try:
            self.db = mysql.connect(
                host=self.hostname,
                database=self.database,
                user=self.username,
                password=self.loginpassword,
                port=self.port,
            )
            if self.db.is_connected():
                self.cursor = self.db.cursor()
        except Error as e:
            if e.errno == 2003 and self.retry_count <= 3:
                messagebox.showwarning("網絡連接", "網絡不可用，無法連線，請檢查網絡連接。按下確認3秒後重試")
                self.retry_count += 1
                slp(3)
                self.connect()
            elif e.errno == 2003:
                messagebox.showerror("退出", "網絡仍然不可用，請檢查網絡連接")
            else:
                print("連接到 MySQL 時出錯:", e)
                raise e

    def close_connection(self):
        if self.db and self.db.is_connected():
            self.cursor.close()
            self.db.close()

    def create_table(self):
        try:
            sql = f"""CREATE TABLE IF NOT EXISTS {self.database_table_name} (  
                        name VARCHAR(255) NOT NULL PRIMARY KEY,
                        addhpcache TINYTEXT NOT NULL,
                        coinlvl TINYTEXT NOT NULL,
                        healthlvl TINYTEXT NOT NULL,
                        swordlvl TINYTEXT NOT NULL,
                        coins MEDIUMTEXT NOT NULL,
                        cu MEDIUMTEXT NOT NULL,
                        cuosf TINYTEXT NOT NULL,
                        darkmode TINYTEXT NOT NULL,
                        darkmodecolor MEDIUMTEXT NOT NULL,
                        difficult TINYTEXT NOT NULL,
                        hp TINYTEXT NOT NULL,
                        langchoose TINYTEXT NOT NULL,
                        monsternum TINYTEXT NOT NULL,
                        password MEDIUMTEXT NOT NULL,
                        playername MEDIUMTEXT NOT NULL,
                        food MEDIUMTEXT NOT NULL,
                        playerhunger MEDIUMTEXT NOT NULL,
                        tick MEDIUMTEXT NOT NULL,
                        online TINYTEXT NOT NULL
                )"""
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as Err:
            print("創建表時出錯:", Err)

    def insert_player_data(self, player_data):
        try:
            sql = f"""INSERT INTO {self.database_table_name} (name, addhpcache, coinlvl, healthlvl, swordlvl, coins, cu, cuosf, darkmode, darkmodecolor, difficult, hp, langchoose, monsternum, password, playername, food, playerhunger, tick, online)  
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, player_data)
            self.db.commit()
        except Exception as Err:
            print(f"插入玩家數據時出錯: {Err}")
            self.db.rollback()

    def check_player_exists(self, plrname):
        try:
            sql = f"SELECT * FROM {self.database_table_name} WHERE name = %s"
            self.cursor.execute(sql, (plrname,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as Err:
            print(f"檢查玩家是否存在時出錯: {Err}")
            return False

    def update_player_data(self, plrname, player_data):
        try:
            sql = f"""UPDATE {self.database_table_name} SET   
                    addhpcache = %s, coinlvl = %s, healthlvl = %s, swordlvl = %s, coins = %s, cu = %s, cuosf = %s, darkmode = %s, darkmodecolor = %s, difficult = %s, hp = %s, langchoose = %s, monsternum = %s, password = %s, playername = %s, food = %s, playerhunger = %s, tick = %s, online = %s  
                    WHERE name = %s"""
            self.cursor.execute(sql, (*player_data, plrname))
            self.db.commit()
        except Exception as Err:
            print(f"更新玩家數據時出錯: {Err}")
            self.db.rollback()

    def get_player_data(self, plrname):
        try:
            sql = f"SELECT addhpcache, coinlvl, healthlvl, swordlvl, coins, cu, cuosf, darkmode, darkmodecolor, difficult, hp, langchoose, monsternum, password, playername, food, playerhunger, tick, online FROM {self.database_table_name} WHERE name = %s"
            self.cursor.execute(sql, (plrname,))
            result = self.cursor.fetchone()
            if result:
                keys = [
                    "addhpcache",
                    "coinlvl",
                    "healthlvl",
                    "swordlvl",
                    "coins",
                    "cu",
                    "cuosf",
                    "darkmode",
                    "darkmodecolor",
                    "difficult",
                    "hp",
                    "langchoose",
                    "monsternum",
                    "password",
                    "playername",
                    "food",
                    "playerhunger",
                    "tick",
                    "online",
                ]
                player_dict = dict(zip(keys, result))
                return player_dict
            else:
                return None
        except Error as Err:
            if Err.errno == 1146:  # Table doesn't exist
                self.create_table()
                return self.get_player_data(plrname)
            else:
                print(f"查詢玩家數據時出錯: {Err}")
                raise Err

    def get_online_players(self):
        sql = f"SELECT name FROM {self.database_table_name} WHERE online = '1'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [row[0] for row in result]  # get players name

    def create_chat_table(self):
        """
        創建聊天消息表
        """
        try:
            sql = """CREATE TABLE IF NOT EXISTS chat_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                timestamp BIGINT NOT NULL,
                INDEX (timestamp)
            )"""
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(f"創建聊天表時出錯: {e}")
            raise e

    def save_chat_message(self, player: str, message: str) -> None:
        """
        保存聊天消息到資料庫
        """
        try:
            sql = "INSERT INTO chat_messages (player, message, timestamp) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (player, message, int(getts())))
            self.db.commit()
        except Exception as e:
            print(f"保存聊天消息時出錯: {e}")
            self.db.rollback()

    def get_chat_messages(self, limit: int = 100, after_timestamp: int = 0) -> list:
        """
        獲取聊天消息
        
        Args:
            limit: 限制返回的消息數量
            after_timestamp: 只返回此時間戳之後的消息
        """
        try:
            if after_timestamp > 0:
                sql = """
                    SELECT player, message, timestamp 
                    FROM chat_messages 
                    WHERE timestamp > %s 
                    ORDER BY timestamp ASC 
                    LIMIT %s
                """
                self.cursor.execute(sql, (after_timestamp, limit))
            else:
                sql = """
                    SELECT player, message, timestamp 
                    FROM chat_messages 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """
                self.cursor.execute(sql, (limit,))
            
            messages = self.cursor.fetchall()

            # 將結果轉換為字典格式
            result = []
            for msg in messages:
                result.append({
                    "player": msg[0],
                    "message": msg[1],
                    "timestamp": msg[2]
                })
            
            # 只有在沒有 after_timestamp 時才需要反轉列表
            return result if after_timestamp > 0 else result[::-1]
        
        except Exception as e:
            print(f"獲取聊天消息時出錯: {e}")
            return []


def upload(
    plrname,
    addhpcache,
    coinlvl,
    healthlvl,
    swordlvl,
    coins,
    cu,
    cuosf,
    darkmode,
    darkmodecolor,
    difficult,
    hp,
    langchoose,
    monsternum,
    password,
    playername,
    food,
    hunger,
    tick,
    online,
):
    db_module = DatabaseModule()
    db_module.connect()
    player_data = get_player_data_tuple(
        addhpcache,
        coinlvl,
        healthlvl,
        swordlvl,
        coins,
        cu,
        cuosf,
        darkmode,
        darkmodecolor,
        difficult,
        hp,
        langchoose,
        monsternum,
        password,
        playername,
        food,
        hunger,
        tick,
        online,
    )

    if not db_module.check_player_exists(plrname):
        thread = threading.Thread(
            target=db_module.insert_player_data, args=((plrname, *player_data),)
        )
    else:
        thread = threading.Thread(
            target=db_module.update_player_data,
            args=(
                plrname,
                player_data,
            ),
        )
    thread.start()
    thread.join()

    db_module.close_connection()


def get(plrname):
    db_module = DatabaseModule()
    db_module.connect()
    data = db_module.get_player_data(plrname)
    db_module.close_connection()
    return data


def check_player_exists(plrname):
    db_module = DatabaseModule()
    db_module.connect()
    res = db_module.check_player_exists(plrname)
    db_module.close_connection()
    return res


def get_online_players():
    db_module = DatabaseModule()
    db_module.connect()
    onlineplrs = db_module.get_online_players()
    db_module.close_connection()
    return onlineplrs


def save_chat_message(player: str, message: str) -> None:
    """
    保存聊天消息到資料庫的外部函數
    """
    db_module = DatabaseModule()
    db_module.connect()
    try:
        db_module.save_chat_message(player, message)
    finally:
        db_module.close_connection()


def get_chat_messages(limit: int = 100, after_timestamp: int = 0) -> list:
    """
    獲取聊天消息的外部函數
    
    Args:
        limit: 限制返回的消息數量
        after_timestamp: 只返回此時間戳之後的消息
    """
    db_module = DatabaseModule()
    db_module.connect()
    try:
        messages = db_module.get_chat_messages(limit, after_timestamp)
        return messages
    finally:
        db_module.close_connection()


def create_chat_table() -> None:
    """
    創建聊天表的外部函數
    """
    db_module = DatabaseModule()
    db_module.connect()
    try:
        db_module.create_chat_table()
    finally:
        db_module.close_connection()
