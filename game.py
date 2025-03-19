import sys
import pickle
from os.path import exists, abspath, dirname, join as path_join
from os import makedirs as md, listdir, remove
from random import randint
import threading
from threading import Thread, Lock
from time import time as getts, sleep as slp
from typing import NoReturn
from atexit import register, unregister
from platform import python_version, system
import asyncio
import hashlib
from shutil import rmtree
from gc import collect as gc_collect
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from subprocess import run
from datetime import datetime

pyversion = "".join(python_version().split(".")[:2])
if f"python{pyversion}._pth" in listdir(dirname(abspath(sys.executable))):
    current_dir = dirname(abspath(__file__))

    if current_dir not in sys.path:
        sys.path.append(current_dir)

system_environment = system().lower()
path_separator = "\\" if system_environment == "windows" else "/"

filename = abspath(__file__).split(path_separator)[-1].replace(".py", "")
firstnrunning = True
starttime = getts()

parent_folder_name = dirname(abspath(__file__)).split(path_separator)[-1]


def delete_pycache():
    """
    刪除所有__pycache__資料夾
    """

    for folder in listdir("."):
        if folder == "__pycache__":
            rmtree(path_join(".", folder))
        elif exists(path_join(".", folder, "__pycache__")):
            rmtree(path_join(".", folder, "__pycache__"))


delete_pycache()


def exi() -> None:
    exit()


try:
    # from cryptography.fernet import Fernet, InvalidToken
    from tkinter import (
        Tk,
        messagebox,
        Button,
        Label,
        Toplevel,
        Entry,
        Text,
        StringVar,
        Scrollbar,
        Frame,
        Checkbutton,
        BooleanVar,
        Radiobutton,
    )
    import mysql.connector
    import requests
    import psutil
    import gdown

    del mysql.connector  # 只是檢查模塊, 此py沒有使用此模塊
    del requests  # 只是檢查模塊, 此py沒有使用此模塊
    del gdown  # 只是檢查模塊, 此py沒有使用此模塊
except ModuleNotFoundError:
    run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            # "cryptography",
            "tk",
            "mysql-connector-python",
            "requests",
            "psutil",
            "gdown",
        ]
    )
    run([sys.executable, __file__])
    exi()

del exi

from module.check_file_update import cfu
from module.returndiff import diff as returndiff
from module.returnhealth import returnishealth, returnmonsterinfo
import module.database.functions as database

# use PE instead of modules if needed
# from extra.PE import cfu, diff as returndiff, returnishealth, returnmonsterinfo, database

if not exists("data"):
    Thread(target=md, args=("data",), daemon=True).start()

# \\\\\\\\\\\\\\\ init variables ///////////////
tick_count = 0
# /////////////// init variables \\\\\\\\\\\\\\\

# \\\\\\\\\\\\\\\ config ///////////////
enable_tps = True
# /////////////// config \\\\\\\\\\\\\\\


class gt:
    """
    遊戲執行緒管理類
    """

    def __init__(self):
        self.save_queue = Queue()
        self.save_worker = Thread(target=self._process_save_queue, daemon=True)
        self.save_worker.start()
        self.last_save_time = 0
        self.save_interval = 0.5  # 最小儲存間隔（秒）

    def _process_save_queue(self):
        while True:
            try:
                save_func = self.save_queue.get()
                current_time = getts()

                # 確保儲存操作之間有足夠間隔
                if current_time - self.last_save_time < self.save_interval:
                    slp(self.save_interval - (current_time - self.last_save_time))

                save_func()
                self.last_save_time = current_time
                self.save_queue.task_done()
            except Exception as e:
                print_log(f"Save queue error: {e}", show_log=True)
            finally:
                slp(0.05)


class monster:
    __slots__ = ("health", "attackage", "name")

    def __init__(self, name, health=None, attackage=None):
        if health is None or attackage is None:
            info = returnmonsterinfo(difficult)
        self.health = info[0] if health is None else health
        self.attackage = info[1] if attackage is None else attackage
        self.name = name
        print_log(
            f"{lang.zombie}{self.name} {lang.spawned}!({lang.shealth[1:]}: {self.health}, {lang.damage}: {self.attackage})"
        )

    def attack(self):
        global hp, add_hp_0_5
        if self.health <= 0 and self in zombies:
            zombies.remove(self)
            print_log(f"{lang.zombie}{self.name} {lang.udied[1:]}!")
        else:
            if randint(1, 2) == 1:
                print_log(
                    f"{playername}{lang.evade}{lang.zombie}{self.name}{lang.success}!"
                )
                # plrsword = int(readfile(cs, "swordlvl"))
                plrsword = int(readfile("swordlvl"))
                if plrsword > 0:
                    monster_health_reduce = 5 * plrsword
                    print_log(
                        f"{playername} {lang.used} {plrsword} {lang.swordtoattack}{lang.zombie}{self.name}. {lang.zombie}{lang.health} - {monster_health_reduce}"
                    )
                    add_hp_0_5 += 1
                    print_log(f"{playername}{lang.s} 0.5 hp + 1 ({lang.two0_5hpto1hp})")
                    if self.health - monster_health_reduce <= 0:
                        self.health = 0
                        if self in zombies:
                            zombies.remove(self)
                            print_log(f"{lang.zombie}{self.name} {lang.udied[1:]}!")
                        del self
                    else:
                        self.health -= monster_health_reduce
            else:
                print_log(
                    f"{playername}{lang.evade}{lang.zombie}{self.name}{lang.failed}，{lang.zombie}{self.name}{lang.attacking[2:]}!"
                )
                mins = int(tick * 0.06)
                hours = 0
                days = 0
                while mins >= 60:
                    hours += 1
                    mins -= 60
                while hours >= 24:
                    days += 1
                    hours -= 24
                if (20 <= hours <= 24) or (0 <= hours <= 4):
                    print_log(f"{self.name} {lang.attacking} {playername}!")
                    hp -= self.attackage
                    print_log(f"{playername}{lang.shealth} - {self.attackage}")
                    # plrsword = int(readfile(cs, "swordlvl"))
                    plrsword = int(readfile("swordlvl"))
                    if plrsword > 0:
                        monster_health_reduce = 5 * plrsword
                        print_log(
                            f"{playername} {lang.used} {plrsword} {lang.swordtoattack}{lang.zombie}{self.name}. {lang.zombie}{lang.health} - {monster_health_reduce}"
                        )
                        add_hp_0_5 += 1
                        print_log(
                            f"{playername}{lang.s} 0.5 hp + 1 ({lang.two0_5hpto1hp})"
                        )
                        if (self.health - monster_health_reduce) <= 0:
                            self.health = 0
                            if self in zombies:
                                zombies.remove(self)
                                print_log(f"{lang.zombie}{self.name} {lang.udied[1:]}!")
                            del self
                        else:
                            self.health -= monster_health_reduce
                            print_log(
                                f"{self.name}{lang.shealth} - {monster_health_reduce}"
                            )
                else:
                    print_log(
                        f"{lang.but}{lang.because}{lang.now}{lang.is1}{lang.morning}，{lang.so}{playername}{lang.willnot}{lang.damaged}"
                    )


# class Player:
#     __slots__ = (
#         "backpack",
#         "health",
#         "name",
#         "hunger",
#         "foods",
#         "healthboost",
#         "attackboost",
#     )

#     def __init__(self, hp, hunger=None, backpack=None, name=None):
#         if name is None:
#             name = plrname or input(lang.typeplayername)
#         if backpack is None:
#             self.backpack = []
#         else:
#             self.backpack = backpack
#         self.health = hp
#         self.name = name
#         self.healthboost = self.backpack.count("health")
#         self.attackboost = self.backpack.count("sword")
#         if hunger is None:
#             self.hunger = 20
#         else:
#             self.hunger = hunger
#         self.foods = self.backpack.count("food")


class UIUpdateManager:
    """
    UI更新管理器
    """

    def __init__(self):
        self.update_queue = Queue()
        self.is_updating = False
        self.last_update = {}
        self.update_worker = Thread(target=self._process_updates, daemon=True)
        self.update_worker.start()

    def _process_updates(self):
        while True:
            try:
                if not self.is_updating:
                    update_func = self.update_queue.get()
                    self.is_updating = True
                    # 使用 queue 來存儲更新函數，然後在主執行緒中執行
                    self._queue_update(update_func)
                    self.update_queue.task_done()
            except Exception as e:
                # 避免在子執行緒中直接呼叫 print_log
                print(f"UI update error: {e}")
            finally:
                slp(0.01)

    def _queue_update(self, update_func):
        try:
            # 確保 UI 更新在主執行緒中執行
            if game.winfo_exists():
                game.after_idle(self._safe_update, update_func)
        except Exception as e:
            print(f"Queue update error: {e}")
        finally:
            self.is_updating = False

    def _safe_update(self, update_func):
        try:
            update_func()
        except Exception as e:
            print(f"Safe update error: {e}")
        finally:
            self.is_updating = False

    def update_label(self, label, text):
        """
        智能更新標籤
        只在內容變更時才更新
        """
        if label not in self.last_update or self.last_update[label] != text:
            self.last_update[label] = text
            self.update_queue.put(lambda: label.config(text=text))

    def update_memory_usage(self):
        """
        更新遊戲記憶體使用量顯示
        """
        try:
            # 獲取當前遊戲進程的記憶體使用
            current_process = psutil.Process()
            game_memory_mb = (
                current_process.memory_info().rss / 1024 / 1024
            )  # 轉換為 MB
            self.update_label(memorylbl, f"{lang.memory}: {game_memory_mb:.3f} MB")
        except Exception as e:
            print_log(f"Memory update error: {e}", show_log=True)


# 初始化 UI 管理器
ui_manager = UIUpdateManager()


class ChatWindow:
    def __init__(self, master):
        # 避免重複開啟聊天視窗
        if chat_window and chat_window.window.winfo_exists():
            chat_window.window.lift()
            chat_window.window.focus_force()
            chat_window.window.attributes("-topmost", True)
            chat_window.window.attributes("-topmost", False)
            return

        self.window = Toplevel(master)
        self.window.title(f"{lang.chat} - {playername}")
        self.window.geometry("400x500")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # 初始化狀態變數
        self.update_lock = Lock()
        self.is_updating = False
        self.sending_messages = {}
        self.message_queue = Queue()
        self.max_concurrent_sends = 1
        self.current_sends = 0
        self.is_processing_queue = False
        self.last_message_timestamp = 0
        self.update_thread = None
        self.displayed_messages = set()  # 新增：追蹤已顯示的訊息
        self.is_running = True  # 新增：用於控制執行緒狀態

        # 創建UI元件
        self._create_ui()

        # 啟動更新執行緒
        self.start_update_thread()

    def _create_ui(self):
        """建立UI元件"""
        # 聊天記錄區域
        self.chat_frame = Frame(self.window)
        self.chat_frame.pack(fill="both", expand=True, padx=5, pady=(5, 40))

        self.scrollbar = Scrollbar(self.chat_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_text = Text(self.chat_frame, yscrollcommand=self.scrollbar.set)
        self.chat_text.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.chat_text.yview)

        # 輸入區域
        self.input_frame = Frame(self.window)
        self.input_frame.pack(fill="x", padx=5, pady=5)

        self.message_entry = Entry(self.input_frame)
        self.message_entry.pack(side="left", fill="x", expand=True)
        self.message_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = Button(
            self.input_frame, text=lang.send, command=self.send_message
        )
        self.send_button.pack(side="right", padx=(5, 0))

    def on_close(self):
        """處理視窗關閉事件"""
        self.is_running = False  # 設置標誌以停止執行緒
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)  # 等待執行緒結束
        self.window.destroy()
        global chat_window
        chat_window = None

    def start_update_thread(self):
        """啟動更新執行緒"""

        def update_worker():
            while self.is_running:
                try:
                    if not self.window.winfo_exists():
                        break
                    self.update_chat()
                    slp(1)  # 每秒更新一次
                except Exception as e:
                    print_log(f"Chat update thread error: {e}", show_log=True)
                    break

        self.update_thread = Thread(target=update_worker, daemon=True)
        self.update_thread.start()

    def update_chat(self):
        """更新聊天記錄"""
        if not self.is_running or self.is_updating:
            return

        if not self.update_lock.acquire(blocking=False):
            return

        try:
            self.is_updating = True

            # 檢查視窗是否還存在
            if not self.window.winfo_exists():
                return

            # 從資料庫獲取新消息
            messages = database.get_chat_messages(
                after_timestamp=self.last_message_timestamp
            )
            if not messages:
                return

            def update_ui():
                if not self.is_running or not self.window.winfo_exists():
                    return

                # 獲取當前聊天框中的所有訊息
                current_messages = self.chat_text.get("1.0", "end-1c").split("\n")
                if current_messages == [""]:
                    current_messages = []

                # 插入新訊息
                new_messages = []
                for msg in messages:
                    formatted_time = datetime.fromtimestamp(msg["timestamp"]).strftime(
                        "%H:%M:%S"
                    )
                    msg_id = f"{formatted_time}{msg['player']}{msg['message']}"

                    # 檢查這條訊息是否已經在發送列表中
                    is_sending = False
                    for sending_msg, (start, end) in self.sending_messages.items():
                        sending_time = formatted_time
                        if (
                            f"[{sending_time}]{msg['player']}: {sending_msg}"
                            == f"[{formatted_time}]{msg['player']}: {msg['message']}"
                        ):
                            is_sending = True
                            break

                    # 如果訊息不在發送列表中且未顯示過，則加入新訊息列表
                    if not is_sending and msg_id not in self.displayed_messages:
                        new_messages.append(
                            f"[{formatted_time}]{msg['player']}: {msg['message']}"
                        )
                        self.displayed_messages.add(msg_id)
                        self.last_message_timestamp = max(
                            self.last_message_timestamp, msg["timestamp"]
                        )

                # 合併現有訊息和新訊息，只保留最後20條
                all_messages = current_messages + new_messages
                if len(all_messages) > 20:
                    all_messages = all_messages[-20:]

                # 清空聊天框並插入最後20條訊息
                self.chat_text.delete("1.0", "end")
                for message in all_messages:
                    if message:  # 確保不是空字串
                        self.chat_text.insert("end", message + "\n")

                # 滾動到最新訊息
                self.chat_text.see("end")

            # 使用 after_idle 而不是 after
            if self.is_running:
                self.window.after_idle(update_ui)

        except Exception as e:
            print_log(f"Chat update error: {e}", show_log=True)
        finally:
            self.is_updating = False
            self.update_lock.release()

    def _send_message(self, message):
        """實際發送訊息"""

        def send():
            try:
                database.save_chat_message(playername, message)

                def update_ui():
                    if not self.window.winfo_exists():
                        return

                    if message in self.sending_messages:
                        # 完全刪除原有訊息和等待中的訊息
                        message_data = self.sending_messages[message]
                        self.chat_text.delete(
                            message_data["message_start"], message_data["message_end"]
                        )
                        del self.sending_messages[message]
                        self.current_sends -= 1

                        # 處理下一條訊息
                        if not self.message_queue.empty():
                            next_message = self.message_queue.get()
                            if next_message in self.sending_messages:
                                next_data = self.sending_messages[next_message]
                                # 刪除等待中的訊息
                                self.chat_text.delete(
                                    next_data["message_start"], next_data["message_end"]
                                )
                                # 插入發送中的訊息
                                message_start = self.chat_text.index("end")
                                self.chat_text.insert(
                                    "end",
                                    f"[{next_data['current_time']}]{playername}: {next_message} (發送中...)\n",
                                )
                                next_data["message_start"] = message_start
                                next_data["message_end"] = self.chat_text.index(
                                    "end-1c"
                                )
                                next_data["status"] = "(發送中...)"
                                self._send_message(next_message)

                if self.is_running:
                    self.window.after_idle(update_ui)

            except Exception as e:

                def show_error():
                    if not self.window.winfo_exists():
                        return

                    if message in self.sending_messages:
                        message_data = self.sending_messages[message]
                        self.chat_text.delete(
                            message_data["message_start"], message_data["message_end"]
                        )
                        self.chat_text.insert(
                            message_data["message_start"],
                            f"[{message_data['current_time']}]{playername}: {message} (發送失敗)\n",
                        )
                        message_data["message_end"] = self.chat_text.index("end-1c")
                        message_data["status"] = "(發送失敗)"
                        del self.sending_messages[message]
                        self.current_sends -= 1

                        # 處理下一條訊息
                        if not self.message_queue.empty():
                            next_message = self.message_queue.get()
                            if next_message in self.sending_messages:
                                next_data = self.sending_messages[next_message]
                                self.chat_text.delete(
                                    next_data["message_start"], next_data["message_end"]
                                )
                                message_start = self.chat_text.index("end")
                                self.chat_text.insert(
                                    "end",
                                    f"[{next_data['current_time']}]{playername}: {next_message} (發送中...)\n",
                                )
                                next_data["message_start"] = message_start
                                next_data["message_end"] = self.chat_text.index(
                                    "end-1c"
                                )
                                next_data["status"] = "(發送中...)"
                                self._send_message(next_message)

                self.window.after_idle(show_error)
                print_log(f"Message send error: {e}", show_log=True)

        Thread(target=send, daemon=True).start()

    def send_message(self):
        """發送訊息"""
        message = self.message_entry.get().strip()
        if not message:
            return

        # 清空輸入框
        self.message_entry.delete(0, "end")

        # 生成訊息時間戳
        current_time = datetime.now().strftime("%H:%M:%S")

        # 決定訊息狀態標記
        status = "(發送中...)" if self.current_sends == 0 else "(等待中...)"

        # 先在聊天框中顯示訊息
        message_start = self.chat_text.index("end")
        self.chat_text.insert(
            "end", f"[{current_time}]{playername}: {message} {status}\n"
        )
        message_end = self.chat_text.index("end-1c")
        self.chat_text.see("end")

        # 記錄訊息位置和資訊
        message_data = {
            "message": message,
            "current_time": current_time,
            "message_start": message_start,
            "message_end": message_end,
            "status": status,
        }
        self.sending_messages[message] = message_data

        # 將訊息加入佇列或直接發送
        if self.current_sends == 0:
            self.current_sends += 1
            self._send_message(message)
        else:
            self.message_queue.put(message)


chat_window: ChatWindow | None = None


def open_chat_window():
    global chat_window
    if chat_window and chat_window.window.winfo_exists():
        chat_window.window.lift()
        chat_window.window.focus_force()
        chat_window.window.attributes("-topmost", True)
        chat_window.window.attributes("-topmost", False)
    else:
        chat_window = ChatWindow(game)


# def readfile(cs: Fernet, filename: str) -> str:
def readfile(filename: str) -> str:
    if not exists(path_join("data", f"{filename}.txt")):
        if filename == "hp":
            content = "100"
        elif filename == "playername":
            askwindow = Toplevel(game)
            askwindow.title("")
            askwindow.resizable(False, False)

            def check_name():
                name = entryvar.get()
                if not name or name == "":
                    return
                if database.check_player_exists(name):
                    # 隱藏原有元件
                    lbl.pack_forget()
                    entry.pack_forget()
                    confirm_btn.pack_forget()

                    # 顯示確認訊息和選擇按鈕
                    exist_label = Label(askwindow, text=lang.playerindatabase)
                    exist_label.pack(pady=5)

                    def use_existing():
                        askwindow.destroy()

                    def go_back():
                        # 移除確認訊息和按鈕
                        exist_label.pack_forget()
                        use_btn.pack_forget()
                        back_btn.pack_forget()

                        # 重新顯示原有元件
                        lbl.pack(pady=5)
                        entry.pack(pady=5)
                        confirm_btn.pack(pady=5)

                    use_btn = Button(
                        askwindow, text=lang.continue_use, command=use_existing
                    )
                    back_btn = Button(askwindow, text=lang.go_back, command=go_back)
                    use_btn.pack(pady=5)
                    back_btn.pack(pady=5)
                else:
                    askwindow.destroy()

            lbl = Label(askwindow, text=lang.typeplayername)
            lbl.pack(pady=5)
            entryvar = StringVar()
            entry = Entry(askwindow, textvariable=entryvar)
            entry.pack(pady=5)
            confirm_btn = Button(askwindow, text="OK", command=check_name)
            confirm_btn.pack(pady=5)

            askwindow.protocol("WM_DELETE_WINDOW", lambda: exit())
            askwindow.transient(game)
            askwindow.grab_set()
            game.wait_window(askwindow)

            content = entryvar.get()
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
        elif filename == "monsternum":
            content = "3"
        elif "monsterinfo" in filename:
            content = ""
        elif filename == "coinlvl":
            content = "1"
        elif filename == "swordlvl":
            content = "1"
        elif filename == "healthlvl":
            content = "1"
        elif filename == "online":
            content = "1"
        elif filename == "hunger":
            content = "20"
        elif filename == "health":
            content = "100"
        else:
            content = "0"

        # ffile.write(cs.encrypt(content.encode()).decode())
        savefile(content, filename)

        return content

    with open(path_join("data", f"{filename}.txt"), "rb") as ffile:
        try:
            result = pickle.load(ffile)
        except EOFError as e:
            print_log(lang.eoferr, show_log=True)
            raise e

    # try:
    #     res = cs.decrypt(result.encode()).decode()
    #     return res
    # except InvalidToken:
    #     print_log(f"{lang.datamayerr_noopentwice}: {filename}")
    #     return readfile(cs, filename)
    # return res

    if isinstance(result, bytes):
        result = result.decode()
    return result


savefile_lock = False


# def savefile(content: str | int | float, cs: Fernet, filename: str) -> None:
def savefile(content: str | int | float, filename: str) -> None:
    global savefile_lock
    if savefile_lock:
        start_lck_runtime = int(getts())

        while savefile_lock:
            current_time = int(getts())
            if current_time - start_lck_runtime >= 5:
                return
            slp(0.3)
    savefile_lock = True

    content = str(content).encode()
    with open(path_join("data", f"{filename}.txt"), "wb") as datafile:
        # encrypt_content = cs.encrypt(content.encode()).decode()
        # datafile.write(encrypt_content)
        pickle.dump(content, datafile)

    savefile_lock = False


# key = b"hhhuuugggooo111333000hugohugohugoeeeeeeeeee="
# cs = Fernet(key)

# langchoose = readfile(cs, "langchoose")
langchoose = readfile("langchoose")
if langchoose == "sc":
    import lang.sc as lang
else:
    import lang.tc as lang

log_window: Toplevel | None = None
game = Tk(className=lang.survivalgame)

log_text_content = ""


def showlog(thenhide: bool = False) -> None:
    """
    顯示log
    """
    global log_window, log_text, log_text_content
    if not thenhide and log_window is not None and log_window.winfo_exists():
        log_window.lift()
        log_window.focus_force()
        log_window.deiconify()
        log_window.attributes("-topmost", True)
        log_window.attributes("-topmost", False)
    else:
        log_window = Toplevel(game)
        log_window.title(lang.log)
        log_window.geometry("400x300")

        log_text = Text(log_window, name=lang.log)
        log_text.insert("end", log_text_content)
        log_text.pack(expand=True, fill="both")

        # 新增滾動條
        scrollbar = Scrollbar(log_window, command=log_text.yview)
        scrollbar.pack(side="right", fill="y")
        log_text.config(yscrollcommand=scrollbar.set)

    if thenhide:
        log_window.withdraw()


def print_log(text: str = "", show_log: bool = False) -> None:
    """
    把記錄放進日誌
    """
    global log_text, log_text_content

    def update_log():
        global log_text, log_text_content
        if show_log:
            showlog()
        text_to_add = text + "\n" if text else "\n"
        log_text_content += text_to_add
        if log_text and log_text.winfo_exists():
            log_text.insert("end", text_to_add)
            log_text.see("end")
            log_text.update()

    # 確保在主執行緒中更新 UI
    if threading.current_thread() is threading.main_thread():
        update_log()
    else:
        game.after_idle(update_log)


def check_for_updates():
    """
    檢查更新
    """
    if cfu() == 1:
        messagebox.showinfo("", lang.cfu1)
        print_log(lang.cfu1)


showlog(thenhide=True)

print_log()  # 打印一行空的東西

# cu = readfile(cs, "cu")
cu = readfile("cu")
# if cu == "1":
#     checkupdate = True
# else:
#     checkupdate = False
checkupdate = cu == "1"

if checkupdate:
    check_for_updates()


hp = int(readfile("hp"))
tick = int(readfile("tick"))
coins = int(float(readfile("coins")))
add_hp_0_5 = int(readfile("addhpcache"))
coinlvl = int(readfile("coinlvl"))
monsternum = int(readfile("monsternum"))
healthlvl = int(readfile("healthlvl"))
swordlvl = int(readfile("swordlvl"))
difficult = int(readfile("difficult"))
darkmodecolor = readfile("darkmodecolor")
darkmode = readfile("darkmode")
cuosf = readfile("cuosf")

can_use_os_system_function = cuosf == "1"
difficultshow = returndiff(difficult)

hunger = int(readfile("hunger"))
health = int(readfile("health"))
food = int(readfile("food"))
playername = readfile("playername")

print_log(f"{lang.player} {playername} {lang.spawned}!")
print_log(f"{playername}{lang.shealth}: {health}")
print_log(f"{playername}{lang.shunger}: {hunger}")
print_log(f"{lang.difficult}: {difficultshow}({difficult})")

gt_obj = gt()

data = database.get(playername)
if data:
    for key in data:
        if key == "online":
            online = "1"
            continue
        value = data[key]
        try:
            int(value)
        except ValueError:
            exec(f"{key} = '{value}'")
        else:
            exec(f"{key} = {value}")
        # savefile(value, cs, key)
        savefile(value, key)
    hunger = playerhunger  # type: ignore # 轉移資料
    del playerhunger  # type: ignore # 轉移資料後刪除
else:
    database.upload(
        playername,
        add_hp_0_5,
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
        online="1",
    )

online = "1"

password  # check if can get password from database


def saveall(exit: bool = False, wait_for_save: bool = False) -> None:
    """
    儲存所有資料
    """

    if exit and not wait_for_save:
        wait_for_save = True

    def saveall_():
        # 先保存到本地文件
        save_batch_1()
        save_batch_2()
        save_batch_3()
        save_batch_4(online_="0" if exit else online)
        save_batch_5()

        # 保存到 MySQL 數據庫
        database.upload(
            playername,
            add_hp_0_5,
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
            online="0" if exit else online,
        )

    if wait_for_save:
        if exit:
            print("Exit -- Saving Data...", end="\r")
        saveall_()
        if exit:
            print("Exit -- Saving Data -- Done")
    else:
        gt_obj.save_queue.put(saveall_)


def restart() -> NoReturn:
    """
    儲存資料並重啟遊戲
    """
    saveall(exit=True)
    if not can_use_os_system_function:
        print_log(f"{lang.cannotusecmd},{lang.plsrestartself}!!", show_log=True)
        return

    print("Restarting...")
    run([sys.executable] + sys.argv, check=True)
    game.destroy()


def saveexit() -> NoReturn:
    """
    儲存資料並退出
    """
    global online, password
    unregister(saveexit)
    online = "0"
    saveall(exit=True)
    try:
        del password
        remove(path_join("data", "password.txt"))
    except:
        pass

    slp(0.5)  # 等待 0.5 秒後再退出
    # quit() # 使用atexit.register不需要手動退出


while True:
    # password is SHA512 hash, "" is this hash, so if password is "", break the loop
    if password == hashlib.sha512("".encode()).hexdigest():
        break
    pw_window = Toplevel(game)
    pw_window.title(lang.pleaseenterpw)
    pw_window.geometry("300x200")
    pw_window.resizable(False, False)

    pw_label = Label(pw_window, text=lang.pleaseenterpw)
    pw_label.pack(pady=10)

    pw_var = StringVar()
    show_pw_var = BooleanVar()
    pw_entry = Entry(pw_window, textvariable=pw_var)
    pw_entry.pack(pady=10)
    pw_entry.focus_set()  # 自動聚焦到密碼輸入框
    is_show_pw = Checkbutton(pw_window, text="顯示密碼", variable=show_pw_var)
    is_show_pw.pack(padx=5)
    show_pw_var.set(True)
    show_pw_var.trace_add(
        "write",
        lambda *args: pw_entry.config(show="*" if not show_pw_var.get() else ""),
    )  # 使用 * 隱藏密碼
    correct = False

    error_label = Label(pw_window, text="", fg="red")
    error_label.pack(pady=5)

    def check_password():
        global correct
        user_entry = pw_var.get()
        if database.hash_password(user_entry) == password:
            pw_window.destroy()
            correct = True

    def on_window_close():
        """當用戶關閉視窗時的處理函數"""
        pw_window.destroy()
        exit()  # 結束遊戲

    confirm_btn = Button(pw_window, text="確認", command=check_password)
    confirm_btn.pack(pady=10)

    # 按Enter鍵也可以確認
    pw_entry.bind("<Return>", lambda event: check_password())

    # 修改視窗關閉處理函數
    pw_window.protocol("WM_DELETE_WINDOW", on_window_close)

    pw_window.transient(game)
    pw_window.grab_set()
    game.wait_window(pw_window)

    if correct:
        break


Thread(target=game.geometry, args=("650x400",), daemon=True).start()

showlog()

isshowhealthadd = returnishealth(difficult)
hplbl = Label(game)
ticklbl = Label(game)
hungerlbl = Label(game)
foodslbl = Label(game)
if isshowhealthadd:
    healthslbl = Label(game)
swordslbl = Label(game)
coinslbl = Label(game)
curcoinlvllbl = Label(game)
onlineplrslbl = Label(game)
memorylbl = Label(game)
memorylbl.place(relx=0.5, rely=0.78, anchor="n")  # 放在線上玩家標籤下方
hplbl.place(relx=0.5, rely=0.1, anchor="n")
ticklbl.place(relx=0.5, rely=0.175, anchor="n")
hungerlbl.place(relx=0.5, rely=0.250, anchor="n")
foodslbl.place(relx=0.5, rely=0.325, anchor="n")
if isshowhealthadd:
    healthslbl.place(relx=0.5, rely=0.4, anchor="n")
swordslbl.place(relx=0.5, rely=0.475, anchor="n")
coinslbl.place(relx=0.5, rely=0.55, anchor="n")
curcoinlvllbl.place(relx=0.5, rely=0.6275, anchor="n")
onlineplrslbl.place(relx=0.5, rely=0.705, anchor="n")

zombies: list[monster] = []


def spawnzombies():
    """
    生成怪物
    """
    for i in range(monsternum):
        name = f"zombie{i}"  # zombie0, zombie1, zombie2, ....
        zombie = monster(name)
        zombies.append(zombie)


def savezombies():
    """
    儲存怪物資訊
    """
    for zombie in zombies:
        index = zombies.index(zombie)  # zombie0 -> 0, zombie1 -> 1, zombie2 -> 2, ....
        # 怪物數據的格式
        zombieinfo = f"{zombie.name}|{zombie.health}|{zombie.attackage}"
        # savefile(zombieinfo, cs, f"zombieinfo{index}")
        savefile(zombieinfo, f"zombieinfo{index}")  # 儲存怪物數據


def readzombies():
    """
    讀取怪物資訊
    """
    files = listdir(path_join("data"))
    for file in files:
        if "zombieinfo" not in file:
            files.remove(file)
    if len(files) == 0:
        spawnzombies()
        savezombies()
        readzombies()
    else:
        for zombieinfo in files:
            index = files.index(zombieinfo)
            exec(f"zombieinfo{index} = readfile(cs, zombieinfo{index})")
            info = zombieinfo.split("|")
            zombie = monster(info[0], info[1], info[2])
            zombies.append(zombie)


def calculate_tps(tick_count, oldticktime):
    """
    計算遊戲TPS
    """
    current_time = getts()
    elapsed_time = current_time - oldticktime

    if elapsed_time >= 1:
        tps = tick_count / elapsed_time
        return tps, current_time, 0
    return None, oldticktime, tick_count


is_refreshing = False


# 新增 UI 更新佇列
ui_update_queue = Queue()
executor = ThreadPoolExecutor(max_workers=2)


async def process_ui_updates():
    """
    處理 UI 更新佇列
    """
    while True:
        try:
            # 非阻塞方式檢查佇列
            while not ui_update_queue.empty():
                update_func = ui_update_queue.get_nowait()
                # 在執行緒池中執行 UI 更新
                await asyncio.get_event_loop().run_in_executor(executor, update_func)
                ui_update_queue.task_done()
        except Exception as e:
            print_log(f"UI update error: {e}", show_log=True)

        await asyncio.sleep(0.05)  # 短暫休息避免 CPU 過載


def refresh():
    """
    刷新文字
    """
    global is_refreshing
    if is_refreshing:
        return

    is_refreshing = True

    try:
        # 計算遊戲時間
        mins = int(tick * 0.06)
        hours = 0
        days = 1
        while mins >= 60:
            hours += 1
            mins -= 60
        while hours >= 24:
            days += 1
            hours -= 24

        hours = str(hours).zfill(2)
        mins = str(mins).zfill(2)

        # 使用 UI 管理器更新標籤
        ui_manager.update_label(hplbl, f"{lang.shealth[1:]}: {hp}")

        if enable_tps:
            try:
                tps_text = f"(tps:{tps:.1f})" if tps > 0 else "(tps:--.--)"
            except:
                tps_text = "(tps:--.--)"
            time_text = f"{lang.day1} {days} {lang.day2} {hours}:{mins} ({tick} tick) {tps_text}"
        else:
            time_text = f"{lang.day1} {days} {lang.day2} {hours}:{mins} ({tick} tick)"
        ui_manager.update_label(ticklbl, time_text)

        ui_manager.update_label(hungerlbl, f"{lang.shunger[1:]}: {hunger} / 20")
        ui_manager.update_label(foodslbl, f"{lang.food}: {food}")
        if isshowhealthadd:
            ui_manager.update_label(healthslbl, f"{lang.healthup}: {healthlvl}")
        ui_manager.update_label(swordslbl, f"{lang.attackup}: {swordlvl}")
        ui_manager.update_label(coinslbl, f"{lang.coins}: {coins}")
        ui_manager.update_label(curcoinlvllbl, f"{lang.coinlvl}: {coinlvl}")
        ui_manager.update_label(onlineplrslbl, f"{lang.onlineplrs}: {onlineplrs}")
        ui_manager.update_memory_usage()  # 更新記憶體使用量

    except Exception as e:
        print_log(f"Refresh error: {e}", show_log=True)
    finally:
        is_refreshing = False


def gametick():
    """
    遊戲主循環
    每0.05秒運行一次
    平均tps為20
    """
    global tick, hp, zombies, hunger, add_hp_0_5, checkupdate
    global oldticktime, tick_count, firstnrunning, tick_time, tps, online, tick_frozen

    try:
        current_tick_time = getts()

        target_frame_time = 0.0475

        # 更新時間戳
        tick_time = current_tick_time

        if not tick_frozen:  # 只在非凍結狀態更新遊戲邏輯
            tick += 1
            tick_count += 1

            # 減少 TPS 計算頻率，每秒只計算一次
            if tick % 20 == 0:
                new_tps, new_oldticktime, new_tick_count = calculate_tps(
                    tick_count, oldticktime
                )
                if new_tps is not None:
                    tps = new_tps
                    oldticktime = new_oldticktime
                    tick_count = new_tick_count

                    if tps > 20.5:
                        target_frame_time = min(0.05, target_frame_time + 0.0005)
                    elif tps < 19.5:
                        target_frame_time = max(0.045, target_frame_time - 0.0005)

            # 處理生命值
            while add_hp_0_5 >= 2:
                add_hp_0_5 -= 2
                hp += 1
                print_log(f"{playername}{lang.shealth} + 1")

            # 每 200 ticks 存檔和處理怪物
            if tick % 200 == 0:
                Thread(target=tick_handler, args=(tick,), daemon=True).start()

        # 無論是否凍結都更新UI
        if tick % 3 == 0:  # 每3個tick更新一次UI
            refresh()

    except Exception as e:
        print_log(f"Gametick error: {e}", show_log=True)
    finally:
        # 使用固定的延遲時間
        game.after(int(target_frame_time * 1000), gametick)


# 初始化全域變數
tps = 0.0
tick_count = 0
oldticktime = getts()
tick_time = getts()
game.after(0, gametick)

if darkmode == "1":
    game.config(bg=darkmodecolor)


# 分批儲存資料
def save_batch_1(hp_=None, tick_=None, coins_=None):
    savefile(hp_ if hp_ is not None else hp, "hp")
    savefile(tick_ if tick_ is not None else tick, "tick")
    savefile(coins_ if coins_ is not None else coins, "coins")


def save_batch_2(add_hp_0_5_=None, langchoose_=None, cu_=None, cuosf_=None):
    savefile(add_hp_0_5_ if add_hp_0_5_ is not None else add_hp_0_5, "addhpcache")
    savefile(langchoose_ if langchoose_ is not None else langchoose, "langchoose")
    savefile(cu_ if cu_ is not None else cu, "cu")
    savefile(cuosf_ if cuosf_ is not None else cuosf, "cuosf")


def save_batch_3(password_=None, darkmode_=None, darkmodecolor_=None, difficult_=None):
    savefile(password_ if password_ is not None else password, "password")
    savefile(darkmode_ if darkmode_ is not None else darkmode, "darkmode")
    savefile(
        darkmodecolor_ if darkmodecolor_ is not None else darkmodecolor, "darkmodecolor"
    )
    savefile(difficult_ if difficult_ is not None else difficult, "difficult")


def save_batch_4(
    monsternum_=None, coinlvl_=None, healthlvl_=None, swordlvl_=None, online_=None
):
    savefile(monsternum_ if monsternum_ is not None else monsternum, "monsternum")
    savefile(coinlvl_ if coinlvl_ is not None else coinlvl, "coinlvl")
    savefile(healthlvl_ if healthlvl_ is not None else healthlvl, "healthlvl")
    savefile(swordlvl_ if swordlvl_ is not None else swordlvl, "swordlvl")
    savefile(online_ if online_ is not None else online, "online")


def save_batch_5(hunger_=None, food_=None, health_=None, playername_=None):
    savefile(hunger_ if hunger_ is not None else hunger, "hunger")
    savefile(food_ if food_ is not None else food, "food")
    savefile(health_ if health_ is not None else health, "health")
    savefile(playername_ if playername_ is not None else playername, "playername")


def tick_handler(tick):
    """
    處理定期儲存和怪物更新
    """
    if tick % 200 != 0:
        return
    global online
    online = "1"
    try:
        # 檢查是否需要儲存
        current_time = getts()
        if current_time - gt_obj.last_save_time >= gt_obj.save_interval:

            # 分批加入儲存佇列
            gt_obj.save_queue.put(save_batch_1)
            gt_obj.save_queue.put(save_batch_2)
            gt_obj.save_queue.put(save_batch_3)
            gt_obj.save_queue.put(save_batch_4)
            gt_obj.save_queue.put(save_batch_5)

            # 怪物資料分批儲存
            for i in range(0, len(zombies), 5):  # 每5個怪物一批
                batch_zombies = zombies[i : i + 5]

                def save_zombies_batch(zombie_batch):
                    for zombie in zombie_batch:
                        index = zombies.index(zombie)
                        zombieinfo = f"{zombie.name}|{zombie.health}|{zombie.attackage}"
                        savefile(zombieinfo, f"zombieinfo{index}")

                gt_obj.save_queue.put(lambda b=batch_zombies: save_zombies_batch(b))

    except Exception as e:
        print_log(f"Tick handler error: {e}", show_log=True)


tick_time = 0


class OnlinePlayersManager:
    """
    線上玩家管理器
    """

    def __init__(self):
        self.lock = Lock()
        self.is_updating = False
        self.last_update_time = 0
        self.update_interval = 15  # 最小更新間隔（秒）


def refresh_online_plrs() -> None:
    """
    刷新onlineplrs
    使用佇列處理資料庫查詢
    """
    global onlineplrs

    def update_online_players():
        # 使用 with 語句確保鎖會被正確釋放
        if not online_players_manager.lock.acquire(blocking=False):
            # 如果無法獲取鎖，表示已經有更新在進行
            return

        try:
            current_time = getts()
            # 檢查是否達到最小更新間隔
            if (
                current_time - online_players_manager.last_update_time
                < online_players_manager.update_interval
            ):
                return

            online_players_manager.is_updating = True

            # 使用異步方式獲取玩家列表
            def fetch_players():
                try:
                    players = database.get_online_players()
                    if players:  # 確保有資料才更新
                        global onlineplrs
                        onlineplrs = ",".join(players)
                        # 使用UI管理器更新標籤，避免直接操作UI
                        ui_manager.update_label(
                            onlineplrslbl, f"{lang.onlineplrs}: {onlineplrs}"
                        )
                except Exception as e:
                    print_log(f"Online players fetch error: {e}", show_log=True)
                finally:
                    online_players_manager.is_updating = False
                    online_players_manager.lock.release()

            # 使用執行緒池執行資料庫查詢
            executor.submit(fetch_players)
            online_players_manager.last_update_time = current_time

        except Exception as e:
            print_log(f"Online players update error: {e}", show_log=True)
        finally:
            online_players_manager.is_updating = False
            online_players_manager.lock.release()

    # 使用執行緒處理資料庫查詢
    Thread(target=update_online_players, daemon=True).start()
    game.after(20 * 1000, refresh_online_plrs)


# 初始化線上玩家管理器
online_players_manager = OnlinePlayersManager()


def get_food() -> None:
    """
    獲取食物
    """
    global food
    food += 1


def eat_food() -> None:
    """
    當玩家的飢餓值低於20且擁有食物時, 吃掉食物
    """
    global hunger, food
    if food > 0 and hunger < 20:
        food -= 1
        hunger += 1


def skip_night() -> None:
    """
    跳過晚上
    但會扣1~5飢餓值
    """
    global tick, hunger
    mins = int(tick * 0.06)
    hours = 0
    days = 0
    while mins >= 60:
        hours += 1
        mins -= 60
    while hours >= 24:
        days += 1
        hours -= 24
    if (18 <= hours <= 24) or (0 <= hours <= 4):
        # skipto_hour = 5  # 05:00
        # _tick = tick
        # _tick -= days * 24000
        # addtick = 24000 - _tick
        # addtick += skipto_hour * 1000  # skip to next day 05:00
        # tick += addtick

        skipto_hour = 5  # 05:00
        todaytick = tick % 24000
        today_remaintick = 24000 - todaytick
        skip_tick = skipto_hour * 1000  # skip to next day 05:00
        tick += today_remaintick + skip_tick

        if difficult == 0:
            return
        reducehunger = randint(1, 5)
        hunger -= reducehunger
        print_log(f"{lang.skippednight}{reducehunger}")


def get_coin() -> None:
    """
    獲取金幣
    """

    def get_coins():
        global coins
        # if coinlvl > 1:
        #     add = 10 ** (coinlvl - 1)
        # else:
        #     add = 1
        add = 10**coinlvl if coinlvl > 0 else 1
        coins += add
        print_log(f"{lang.coinsget1}{add}{lang.coinsget2}{coins})")

    Thread(target=get_coins, daemon=True).start()


def buy(obj: str) -> None:
    """
    購買加成
    """
    global coins, healthlvl, swordlvl
    if obj == "h":
        if coins >= 5:
            healthlvl += 1
            coins -= 5
        else:
            print_log(lang.e5ceq1h)
    elif obj == "s":
        if coins >= 5:
            swordlvl += 1
            coins -= 5
        else:
            print_log(lang.e5ceq1s)


def addhealth() -> None:
    """
    增加生命值
    """
    global hunger, hp, food
    if food > 0 and hunger < 20:
        food -= 1
        hunger += 1
        print_log(f"{playername}{lang.atefood1}{food}{lang.atefood2}{hunger}")

    if hunger > 16 and hp < 100:
        if difficult != 0:
            hunger -= 1
        if difficult == 0:
            addhp = 1
        elif difficult == 1:
            addhp = 2
        elif difficult == 2:
            addhp = 4
        elif difficult == 3:
            addhp = 1
        if healthlvl > 0 and isshowhealthadd:
            addhp *= healthlvl + 1

        hp += addhp
        print_log(
            f"{playername} {lang.shunger} - 1\n{playername} {lang.shealth} + {addhp}"
        )


game_settings_window = None


def opengamesettings() -> None:
    """
    打開遊戲設定
    """
    global game_settings_window
    if game_settings_window and game_settings_window.winfo_exists():
        game_settings_window.lift()
        game_settings_window.focus_force()
        game_settings_window.attributes("-topmost", True)
        game_settings_window.attributes("-topmost", False)
    else:
        game_settings_window = Toplevel(game)
        game_settings_window.title(lang.gamesettings)
        game_settings_window.geometry("400x300")
        if darkmode == "1":
            game_settings_window.config(bg=darkmodecolor)
        pwentry = Entry(game_settings_window)
        diffentry = Entry(game_settings_window)
        monsternumentry = Entry(game_settings_window)
        darkmodecolor_entry = Entry(game_settings_window)
        pwentry.place(relx=0.05, rely=0.1, anchor="w")
        diffentry.place(relx=0.05, rely=0.8, anchor="w")
        monsternumentry.place(relx=0.05, rely=0.95, anchor="w")
        darkmodecolor_entry.place(relx=0.05, rely=0.5, anchor="w")
        curlanglbl = Label(game_settings_window)
        curthemelbl = Label(game_settings_window)
        curupdatelbl = Label(game_settings_window)
        curdarkmodecolorlbl = Label(game_settings_window)
        curdifflbl = Label(game_settings_window)
        curmonsternumlbl = Label(game_settings_window)
        curlanglbl.place(relx=0.1, rely=0.2, anchor="w")
        curthemelbl.place(relx=0.1, rely=0.3, anchor="w")
        curupdatelbl.place(relx=0.1, rely=0.4, anchor="w")
        curdarkmodecolorlbl.place(relx=0.1, rely=0.6, anchor="w")
        curdifflbl.place(relx=0.1, rely=0.7, anchor="w")
        curmonsternumlbl.place(relx=0.1, rely=0.875, anchor="w")

        def refreshgamesettings() -> None:
            """
            刷新文字
            """
            curlanglbl.config(text=f"{lang.curlanguage}: {langchoose}")
            curthemelbl.config(text=f"{lang.curtheme}: {darkmode}")
            curupdatelbl.config(text=f"{lang.curupdate}: {checkupdate}")
            curdarkmodecolorlbl.config(
                text=f"{lang.curdarkthemecolor}: {darkmodecolor}"
            )
            curdifflbl.config(text=f"{lang.difficult}: {difficultshow}({difficult})")
            curmonsternumlbl.config(
                text=f"{lang.curmonsternum1} {monsternum} {lang.curmonsternum2}"
            )
            game_settings_window.after(200, refreshgamesettings)

        game_settings_window.after(0, refreshgamesettings)

        def setpw() -> None:
            global usersetpw, password
            usersetpw = pwentry.get()
            if password == usersetpw:
                print_log(lang.samepwnochange)
            else:
                password = usersetpw
                print_log(lang.changedpw, show_log=True)
                saveall()

        def changelang() -> None:
            global langchoose, lang
            language_choices = [
                {"name": "繁體中文", "value": "tc"},
                {"name": "简体中文", "value": "sc"},
            ]

            # 創建語言選擇視窗
            lang_window = Toplevel(game)
            lang_window.title(lang.curlanguage)
            lang_window.geometry("300x200")
            lang_window.resizable(False, False)

            # 如果啟用了深色模式，設置背景顏色
            if darkmode == "1":
                lang_window.config(bg=darkmodecolor)

            # 創建標題標籤
            title_label = Label(
                lang_window, text=lang.curlanguage, font=("Arial", 14, "bold")
            )
            title_label.pack(pady=10)

            # 創建語言選擇框架
            lang_frame = Frame(lang_window)
            lang_frame.pack(pady=10)

            # 當前選擇的語言
            selected_lang = StringVar()
            selected_lang.set(langchoose)

            # 語言選項
            for lang in language_choices:
                Radiobutton(
                    lang_frame,
                    text=lang["name"],
                    variable=selected_lang,
                    value=lang["value"],
                ).pack(anchor="w", pady=5)

            # 確認按鈕
            def confirm_lang():
                global langchoose
                langchoose = selected_lang.get()
                lang_window.destroy()
                saveall()

            confirm_button = Button(
                lang_window, text=lang.confirm, command=confirm_lang
            )
            confirm_button.pack(pady=10)

            # 讓視窗置頂
            lang_window.transient(game)
            lang_window.grab_set()
            game.wait_window(lang_window)

            restart()

        def changetheme() -> None:
            global darkmode
            if darkmode == "1":
                darkmode = "0"
                color = Button(game_settings_window).cget("background")
                game_settings_window.config(bg=color)
                game.config(bg=color)
            else:
                darkmode = "1"
                game_settings_window.config(bg=darkmodecolor)
                game.config(bg=darkmodecolor)
            saveall()

        def changeupdate() -> None:
            global cu, checkupdate
            if cu == "1":
                cu = "0"
                checkupdate = False
            else:
                cu = "1"
                checkupdate = True
            saveall()

        def setdarkthemecolor() -> None:
            global darkmodecolor, darkmode
            hexcode = darkmodecolor_entry.get()
            if (not len(hexcode) == 7) or ("#" not in hexcode):
                print_log(f"{lang.hexcodeerr}: {hexcode}")
            else:
                darkmodecolor = hexcode
                if darkmode == "0":
                    darkmode = "1"
                game_settings_window.config(bg=darkmodecolor)
                game.config(bg=darkmodecolor)
                saveall()

        def setdifficulty() -> None:
            global difficult
            diff = diffentry.get()
            try:
                diff = int(diff)
            except ValueError:
                return print_log(
                    f"{lang.difficult}{lang.must}{lang.is1} 0({lang.peaceful}) 1({lang.easy}) 2({lang.normal}) 3({lang.diff})"
                )
            except Exception as err:
                print_log(err)
                input(lang.okpressenterexit[1:])
                quit("Err exit")
            else:
                if diff in (0, 1, 2, 3):
                    if difficult == diff:
                        return print_log("")
                    difficult = diff
                    restart()
                else:
                    return print_log(
                        f"{lang.difficult}{lang.must}{lang.is1} 0({lang.peaceful}) 1({lang.easy}) 2({lang.normal}) 3({lang.diff})"
                    )

        def setmonsternum() -> None:
            num = monsternumentry.get()
            try:
                num = int(num)
            except ValueError:
                return print_log(f"{lang.must}{lang.is1}{lang.num}!")
            except Exception as err:
                input(err)
                quit(err)
            else:
                global monsternum
                if num < 1:
                    return print_log(f"{lang.num}{lang.must}{lang.is1}{lang.morethan}1")
                if num == monsternum:
                    return print_log(f"{lang.num}{lang.samepwnochange[2:]}")
                if num < monsternum:
                    res = messagebox.askquestion(
                        f"{lang.num}{lang.smallerthan}{lang.cur}{lang.s}{lang.num}",
                        f"{lang.udied[0]}{lang.s}{lang.num}{lang.smallerthan}{lang.cur}{lang.s}{lang.num}({lang.will}{lang.delete}{lang.data})",
                        icon="warning",
                    )
                else:
                    res = "yes"
                if res == "yes":
                    if num < monsternum:
                        f = listdir(path_join("data"))
                        files = []
                        for file in f:
                            if "zombieinfo" in file:
                                files.append(file)
                        for file in files:
                            if exists(path_join("data", file)):
                                remove(path_join("data", file))
                    monsternum = num
                    restart()

        Button(game_settings_window, text=lang.resetpw, command=setpw).place(
            relx=0.95, rely=0.1, anchor="e"
        )

        Button(game_settings_window, text=lang.changelang, command=changelang).place(
            relx=0.95, rely=0.2, anchor="e"
        )

        Button(game_settings_window, text=lang.changetheme, command=changetheme).place(
            relx=0.95, rely=0.3, anchor="e"
        )

        Button(
            game_settings_window, text=lang.changeupdate, command=changeupdate
        ).place(relx=0.95, rely=0.4, anchor="e")

        Button(
            game_settings_window, text=lang.setdarkthemecolor, command=setdarkthemecolor
        ).place(relx=0.9, rely=0.5, anchor="e")

        Button(game_settings_window, text=lang.changediff, command=setdifficulty).place(
            relx=0.95, rely=0.8, anchor="e"
        )

        Button(
            game_settings_window, text=lang.setmonsternum, command=setmonsternum
        ).place(relx=0.9, rely=0.95, anchor="e")


def upgradecoinlvl() -> None:
    global coins, coinlvl
    needcoin = 10 ** (coinlvl + 2)
    if coins >= needcoin:
        coins -= needcoin
        coinlvl += 1
        saveall()
    else:
        print_log(
            f"{lang.notenough}{lang.coins}{lang.swordtoattack[2]}{lang.buys[:2]}({lang.need}{needcoin}{lang.coins})"
        )


tick_frozen = False
console_window: None | Toplevel = None


def open_console_window():
    global console_window, output_text
    if not console_window or not console_window.winfo_exists():
        console_window = Toplevel(game)
        console_window.title("Console")
        console_window.geometry("500x300")

        # 創建一個frame來容納output_text和scrollbar
        text_frame = Frame(console_window)
        text_frame.pack(fill="both", expand=True, padx=5, pady=(5, 40))  # 底部加大間隔

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        output_text = Text(text_frame, yscrollcommand=scrollbar.set)
        output_text.pack(fill="both", expand=True)
        scrollbar.config(command=output_text.yview)

        command_entry = Entry(console_window)
        command_entry.place(relx=0.5, rely=0.9, anchor="center")

        def execute_and_clear(event):
            command = command_entry.get()
            execute_command(command)
            if command == "exit":
                return
            command_entry.delete(0, "end")
            output_text.see("end")

        command_entry.bind("<Return>", execute_and_clear)


def tick_freeze():
    global tick_frozen
    tick_frozen = True


def tick_unfreeze():
    global tick_frozen
    tick_frozen = False


command_list = {
    "exit": "Exit the console",
    "help": "Show this help",
    "clear": "Clear the console",
    "cls": "Clear the console",
    "restart": "Restart the game",
    "saveall": "Save all data",
    "tick freeze": "Freeze the tick",
    "tick unfreeze": "Unfreeze the tick",
    "tick get": "Get the tick",
}


def execute_command(command):
    global console_window, output_text
    if command == "exit":
        console_window.destroy()
        console_window = None
        return
    response, func = command_handler(command)
    if func:
        func()
    output_text.insert("end", f"{command}\n↪️{response}\n")


def command_handler(command):
    command = command.replace("/", "").lower()
    if command in ("help", "h", "?"):
        text = "Available commands:\n"
        for command, description in command_list.items():
            text += f"{command} - {description}\n"
        return (text, None)
    elif command == "tick get":
        return (f"Current tick: {tick}", None)
    elif command == "tick freeze":
        return (None, tick_freeze)
    elif command == "tick unfreeze":
        return (None, tick_unfreeze)
    elif command == "restart":
        return (None, restart)
    elif command == "saveall":
        return (None, saveall)
    elif command == "clear" or command == "cls":
        return (None, lambda: output_text.delete(0, "end"))
    else:
        return (f"Unknown command: {command}", None)


# Button(game, text=lang.addhealth, command=addhealth).place(
#     relx=0.2, rely=0.005, anchor="ne"
# )
# Button(game, text=lang.eatfood, command=eat_food).place(relx=0.2, rely=0.1, anchor="ne")
# Button(game, text=lang.getfood, command=get_food).place(relx=0.2, rely=0.2, anchor="ne")
# Button(game, text=lang.skipnight, command=skip_night).place(
#     relx=0.2, rely=0.3, anchor="ne"
# )
# if isshowhealthadd:
#     Button(game, text=lang.buyh, command=lambda: buy("h")).place(
#         relx=0.22, rely=0.4, anchor="ne"  # 字比較長，特殊按鈕，relx0.22
#     )
# Button(game, text=lang.buys, command=lambda: buy("s")).place(
#     relx=0.22, rely=0.5, anchor="ne"  # 字比較長，特殊按鈕，relx0.22
# )
# Button(game, text=lang.getcoin, command=get_coin).place(relx=0.2, rely=0.6, anchor="ne")
# Button(game, text=lang.opengamesettings, command=opengamesettings).place(
#     relx=0.22, rely=0.7, anchor="ne"  # 字比較長，特殊按鈕，relx0.22
# )

# Button(game, text=lang.upgradecoinlvl, command=upgradecoinlvl).place(
#     relx=0.22, rely=0.8, anchor="ne"  # 字比較長，特殊按鈕，relx0.22
# )

# Button(game, text=lang.log, command=showlog).place(relx=0.2, rely=0.9, anchor="ne")

Buttons = [
    {
        "text": lang.addhealth,
        "command": addhealth,
        "special": False,
        "positiony": 0.005,
    },
    {
        "text": lang.eatfood,
        "command": eat_food,
        "special": False,
        "positiony": 0.1,
    },
    {
        "text": lang.getfood,
        "command": get_food,
        "special": False,
        "positiony": 0.2,
    },
    {
        "text": lang.skipnight,
        "command": skip_night,
        "special": False,
        "positiony": 0.3,
    },
    {
        "text": lang.buyh,
        "command": lambda: buy("h"),
        "special": True,
        "positiony": 0.4,
    },
    {
        "text": lang.buys,
        "command": lambda: buy("s"),
        "special": True,
        "positiony": 0.5,
    },
    {
        "text": lang.getcoin,
        "command": get_coin,
        "special": False,
        "positiony": 0.6,
    },
    {
        "text": lang.opengamesettings,
        "command": opengamesettings,
        "special": True,
        "positiony": 0.7,
    },
    {
        "text": lang.upgradecoinlvl,
        "command": upgradecoinlvl,
        "special": True,
        "positiony": 0.8,
    },
    {
        "text": lang.log,
        "command": showlog,
        "special": False,
        "positiony": 0.9,
        "positionx": 0.2,
    },
    {
        "text": lang.gccollect,
        "command": gc_collect,
        "special": False,
        "positiony": 0.9,
        "positionx": 0.4,
    },
    {
        "text": lang.checkupdate,
        "command": check_for_updates,
        "special": False,
        "positiony": 0.9,
        "positionx": 0.9,
    },
    {
        "text": "Console",
        "command": open_console_window,
        "special": False,
        "positiony": 0.8,
        "positionx": 0.9,
    },
    {
        "text": lang.chat,
        "command": lambda: ChatWindow(game),
        "special": False,
        "positiony": 0.8,
        "positionx": 0.7,
    },
]


for button in Buttons:
    if button["special"] and not button.get("positionx"):
        relx = 0.22
    elif not button.get("positionx"):
        relx = 0.2
    else:
        relx = button["positionx"]

    Button(game, text=button["text"], command=button["command"]).place(
        relx=relx,
        rely=button["positiony"],
        anchor="ne",
    )


def popup_window():
    game.focus_force()
    game.attributes("-topmost", True)
    game.attributes("-topmost", False)


onlineplrs = lang.onlineplrs[:2] + lang.loadedgame[2:4]
game.after(5000, refresh_online_plrs)
game.after(500, popup_window)

if difficult != 0:
    print_log(lang.spawnedzombies)
    spawnzombies()
else:
    print_log(f"{lang.peaceful}{lang.mode}, {lang.so}{lang.willnot}{lang.spawnzombies}")

# game.protocol("WM_DELETE_WINDOW", saveexit)
register(saveexit)  # 改用atexit.register

try:
    game.mainloop()
except KeyboardInterrupt:
    saveexit()
