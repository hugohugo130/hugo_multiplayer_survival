import mysql.connector as mysql
from mysql.connector import Error
import threading
from os.path import exists
import pickle


class DatabaseModule:
    def __init__(self):
        self.hostname = "i4q.h.filess.io"
        self.database = "SurvivalGameDatabase_waveleast"
        self.port = "3307"
        self.username = "SurvivalGameDatabase_waveleast"
        self.loginpassword = "26c2e76ce7825addd2ef214dd23636b04d375a3a"
        self.database_table_name = "players"
        self.db = None
        self.cursor = None

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


class L:
    def __init__(self):
        self.cfu1 = "檢測到更新!請執行game_updater.py去更新哦~"
        self.pressentertoquit = "直接點擊Enter退出遊戲(輸入任何東西繼續遊戲)"
        self.cannotusecmd = "由於無法使用os.system功能,無法進行操作"
        self.stopdlive = "停止下載直播"
        self.playlive = "播放直播(自動下載直播)"
        self.openxztvlive = "打開XiaoziTV直播"
        self.preparingplive = "正在準備播放直播..."
        self.notdlive = "沒有正在下載直播"
        self.stoppeddlive = "已停止下載直播"
        self.waitingvideod = "正在等待影片開始下載..."
        self.videonotd = "影片沒有準備下載,已停止播放"
        self.opengamesettings = "打開遊戲設定"
        self.resetpw = "設定密碼 (留空清除密碼)"
        self.gamesettings = "遊戲設定"
        self.getcoin = "獲取金幣"
        self.buys = "購買攻擊加成"
        self.buyh = "購買回血加成"
        self.skipnight = "跳過晚上"
        self.getfood = "獲取食物"
        self.eatfood = "吃掉食物"
        self.e5ceq1s = "5個金幣 = 1個攻擊加成"
        self.e5ceq1h = "5個金幣 = 1個回血加成"
        self.coinsget1 = "金幣 + "
        self.coinsget2 = " (擁有金幣: "
        self.skippednight = "已跳過晚上, 飢餓值 - "
        self.atefood1 = " 吃了一個食物. 現在他有 "
        self.atefood2 = " 個食物. 他的飢餓值: "
        self.gotfood1 = " 獲得了一個食物. 現在他有 "
        self.gotfood2 = " 個食物"
        self.toomanyhealth = " 太多血了 "
        self.settomax = "設定成最大值"
        self.shealth = "的血量"
        self.udied = "你死了"
        self.urevive = "你復活了"
        self.player = "玩家"
        self.spawned = "生成了"
        self.shunger = "的飢餓值"
        self.zombie = "怪物"
        self.two0_5hpto1hp = "達到2個自動增加1血量"
        self.s = "的"
        self.used = "用了"
        self.swordtoattack = "個劍去打"
        self.health = "血量"
        self.attacking = "正在攻擊"
        self.evade = "躲避"
        self.failed = "失敗"
        self.being = "正在被"
        self.success = "成功"
        self.coins = "金幣"
        self.attackup = "攻擊加成"
        self.healthup = "回血加成"
        self.food = "食物"
        self.day1 = "第"
        self.day2 = "天"
        self.dataerr = "data數據出錯"
        self.survivalgame = "生存遊戲"
        self.pwerr = "密碼錯誤, 錯誤次數:"
        self.remain = "剩下"
        self.times = "次機會"
        self.pwcorrect = "密碼正確"
        self.okpressenterexit = "好吧按下Enter退出"
        self.destroyfailed = "毀滅失敗"
        self.errtoomanydestroyingpc = "錯誤次數太多, 正在毀滅您的電腦"
        self.pleaseenterpw = "請輸入密碼:"
        self.plsrestartself = "請手動重啟"
        self.curlanguage = "目前語言"
        self.changelang = "切換語言 (會重啟)"
        self.changetheme = "切換深色/淺色"
        self.curtheme = "目前背景顏色(1=深色,0=淺色)"
        self.changeupdate = "切換是否檢查更新"
        self.curupdate = "是否檢查更新"
        self.setdarkthemecolor = "設定深色背景的顏色(hex code)"
        self.curdarkthemecolor = "目前深色背景的顏色(hex code)"
        self.hexcodeerr = "hex code必須是#<6位數的hexcode>, 例子: #000000 但你輸入的是"
        self.samepwnochange = "密碼一樣，不需要修改"
        self.changedpw = "已修改密碼,重啟即需要使用密碼進入遊戲"
        self.difficult = "難度"
        self.peaceful = "和平"
        self.easy = "簡單"
        self.normal = "普通"
        self.diff = "困難"
        self.must = "必須"
        self.is1 = "是"
        self.changediff = "切換遊戲難度(會重啟)"
        self.addhealth = "增加血量"
        self.damage = "攻擊力"
        self.curmonsternum1 = "已設定有"
        self.curmonsternum2 = "個怪物"
        self.num = "數字"
        self.smallerthan = "小於"
        self.cur = "目前"
        self.setmonsternum = "設定怪物數量"
        self.but = "但"
        self.because = "由於"
        self.now = "現在"
        self.morning = "早上"
        self.so = "所以"
        self.will = "會"
        self.willnot = "不" + self.will
        self.damaged = "扣血"
        self.delete = "刪除"
        self.data = "資料"
        self.toomanyhunger = " 太多飢餓值了 "
        self.morethan = "大於"
        self.upgradecoinlvl = "購買金幣加成"
        self.notenough = "不夠"
        self.need = "需要"
        self.coinlvl = "金幣加成"
        self.typeplayername = "請輸入你的玩家名 (以後不可更改):"
        self.playerindatabase = "此玩家名的玩家的數據存在於數據庫，是否繼續?"
        self.usedtime = "用時"
        self.loadedgame = "遊戲加載完畢"
        self.sec = "秒"
        self.onlineplrs = "正在遊玩的玩家"
        self.datamayerr_noopentwice = "數據可能出錯了，或者你多開遊戲，請不要這樣做"
        self.exiting_noclosewindow = "正在退出遊戲... 請不要關閉黑色視窗"
        self.log = "日誌"
        self.mode = "模式"
        self.spawnedzombies = "生成了怪物"
        self.spawnzombies = self.spawnedzombies.replace(self.used[-1], "")


class Database:
    def upload(
        self,
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
        playerhunger,
        tick,
        online,
    ):
        db_module = DatabaseModule()
        db_module.connect()
        player_data = (
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
            playerhunger,
            tick,
            online,
        )

        if not db_module.check_player_exists(plrname):
            thread = threading.Thread(
                target=db_module.insert_player_data, args=((plrname, *player_data),)
            )
            thread.start()
            thread.join()
        else:
            thread = threading.Thread(
                target=db_module.update_player_data, args=(plrname, player_data)
            )
            thread.start()
            thread.join()

        db_module.close_connection()

    def get(self, plrname):
        db_module = DatabaseModule()
        db_module.connect()
        data = db_module.get_player_data(plrname)
        db_module.close_connection()
        return data

    def check_player_exists(self, plrname):
        db_module = DatabaseModule()
        db_module.connect()
        res = db_module.check_player_exists(plrname)
        db_module.close_connection()
        return res

    def get_online_players(self):
        db_module = DatabaseModule()
        db_module.connect()
        onlineplrs = db_module.get_online_players()
        db_module.close_connection()
        return onlineplrs


# ========================================


def cfu():
    from os.path import exists

    try:
        from requests import get
    except ModuleNotFoundError:
        from subprocess import run
        from sys import executable

        run([executable, "-m", "pip", "install", "requests"])
        from requests import get

    link = [
        "https://pastebin.com/17ftWr12",  # game.py ------------------https://pastebin.com/edit/17ftWr12
        "https://pastebin.com/N1LyJ1Kq",  # functions.py -------------https://pastebin.com/edit/N1LyJ1Kq
        "https://pastebin.com/4vEnTHBq",  # check_file_update.py -----https://pastebin.com/edit/4vEnTHBq
        "https://pastebin.com/Vrqgd4rP",  # returndiff.py ------------https://pastebin.com/edit/Vrqgd4rP
        "https://pastebin.com/ZFuDC6dR",  # returnhealth.py ----------https://pastebin.com/edit/ZFuDC6dR
        "https://pastebin.com/pG103Stf",  # sc.py --------------------https://pastebin.com/edit/pG103Stf
        "https://pastebin.com/gj01BCVh",  # tc.py --------------------https://pastebin.com/edit/gj01BCVh
    ]

    filename = [
        "game.py",
        "module\\database\\functions.py",
        "module\\check_file_update.py",
        "module\\returndiff.py",
        "module\\returnhealth.py",
        "lang\\sc.py",
        "lang\\tc.py",
    ]

    for l in link:
        if "raw" not in l:
            lid = l.split("/")[-1]
            _l = f"https://pastebin.com/raw/{lid}"
            link[link.index(l)] = _l

    update = []

    for curfilename in filename:
        if "\\" not in curfilename:
            curfilename_ = curfilename
        else:
            curfilename_ = curfilename.split("\\")[-1]
        latestfile = get(link[filename.index(curfilename)]).content
        if exists(curfilename):
            with open(curfilename, "rb") as gamefile:
                gamefilec = gamefile.read()
            if gamefilec != latestfile:
                update.append(curfilename_)
        else:
            update.append(curfilename_)
    return 1 if len(update) > 0 else 0


def diff(dif):
    # key = b"hhhuuugggooo111333000hugohugohugoeeeeeeeeee="
    # cs = Fernet(key)

    # def readfile(cs: object, filename: str):
    def readfile(filename: str):
        if not exists(f"data\\{filename}.txt"):
            a = open(f"data\\{filename}.txt", "w")
            if filename == "hp":
                content = "100"
            elif filename == "playerinfo":
                content = "Player|.20"
            elif filename == "password":
                content = ""
            elif filename == "cu":
                content = "1"
            elif filename == "cuosf":
                content = "1"
            elif filename == "langchoose":
                content = "tc"
            elif filename == "darkmodecolor":
                content = "#000000"
            elif filename == "difficult":
                content = "1"
            else:
                content = "0"
            # a.write(cs.encrypt(content.encode()).decode())
            pickle.dump(content, a)
            a.close()
        with open(f"data\\{filename}.txt", "rb") as ffile:
            # result = ffile.read()
            result = pickle.load(ffile)
        # return cs.decrypt(result.encode()).decode()
        return result

    # langchoose = readfile(cs, "langchoose")
    langchoose = readfile("langchoose")
    if langchoose == "sc":
        import lang.sc as lang
    else:
        import lang.tc as lang
    if dif == 0:
        return lang.peaceful
    if dif == 1:
        return lang.easy
    if dif == 2:
        return lang.normal
    else:
        return lang.diff


def returnishealth(diff):
    if diff == 3:
        return False
    else:
        return True


def returnmonsterinfo(diff):
    if diff == 1:
        health = 50
        attackage = 5
    elif diff == 2:
        health = 100
        attackage = 15
    elif diff == 3:
        health = 1000
        attackage = 99
    if diff in (1, 2, 3):
        return [health, attackage]


lang = L()
database = Database()
