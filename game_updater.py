from os.path import exists
from os import makedirs as md, getcwd
import threading
import os
import zipfile
import tempfile
import shutil

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import gdown
except ModuleNotFoundError:
    from subprocess import run
    from sys import executable

    run([executable, "-m", "pip", "install", "tk", "gdown"])

    import tkinter as tk
    from tkinter import filedialog
    import gdown

# ===============config========================
sc = False
# ===============Advanced Config===============
gdrive_id = "1TK8O5OhxbUC29qHD2Qm1TId8bR37CmhX"
ignore_list = [
    "zip",
    "game_updater",
    "dev",
    "requirements",
    "__pycache__",
    "pyc",
    "output",
    "data",
    "decrypt",
]


def update():
    # 建立臨時資料夾
    temp_dir = os.path.join(tempfile.gettempdir(), "game_temp")
    if exists(temp_dir):
        shutil.rmtree(temp_dir)
    md(temp_dir)
    zip_path = os.path.join(temp_dir, "game_files.zip")

    # 刪除現有檔案（排除包含ignore_list中關鍵字的檔案）
    if messagebox.askyesno("確認", "是否要刪除現有檔案？(不會刪除data資料夾)"):
        for root, dirs, files in os.walk(installpath, topdown=False):
            # 刪除檔案
            for name in files:
                if not any(keyword in name for keyword in ignore_list):
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        if sc:
                            text = f"删除文件失败 {name}: {str(e)}"
                        else:
                            text = f"刪除檔案失敗 {name}: {str(e)}"
                        history.insert(tk.END, text + "\n")

            # 刪除資料夾（如果為空）
            for name in dirs:
                if not any(keyword in name for keyword in ignore_list):
                    try:
                        dir_path = os.path.join(root, name)
                        if not os.listdir(dir_path):  # 確認資料夾是空的
                            os.rmdir(dir_path)
                    except Exception as e:
                        if sc:
                            text = f"删除文件夹失败 {name}: {str(e)}"
                        else:
                            text = f"刪除資料夾失敗 {name}: {str(e)}"
                        history.insert(tk.END, text + "\n")

    # 下載ZIP檔案
    history.insert(tk.END, "正在下載ZIP檔案...\n" if not sc else "正在下载zip档案...\n")
    try:
        gdown.download(f"https://drive.google.com/uc?id={gdrive_id}", zip_path)
    except Exception as e:
        if sc:
            text = f"下载失败: {str(e)}"
        else:
            text = f"下載失敗: {str(e)}"
        history.insert(tk.END, text + "\n")
        return
    history.delete(1.0, tk.END)

    # 驗證檔案大小
    if os.path.getsize(zip_path) < 1000:  # 如果檔案小於1KB
        if sc:
            text = "下载似乎不完整，请检查连接！"
        else:
            text = "下載似乎不完整，請檢查連接！"
        history.insert(tk.END, text + "\n")
        return

    # 解壓縮檔案
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(installpath)  # 直接解壓到安裝路徑
    except Exception as e:
        if sc:
            text = f"解压失败: {str(e)}"
        else:
            text = f"解壓失敗: {str(e)}"
        history.insert(tk.END, text + "\n")
        return

    # 清理暫存檔案
    shutil.rmtree(temp_dir)
    if sc:
        text = "更新完成！"
    else:
        text = "更新完成！"
    history.insert(tk.END, text + "\n")
    history.insert(tk.END, "=" * 55 + "\n")
    global running
    running = False


def updategame():
    global running, history
    if not running:
        running = True
        history.delete(1.0, tk.END)
        threading.Thread(target=update).start()


installpath = getcwd()
updater = tk.Tk(className="updater")
updater.geometry("500x300")
history_frame = tk.LabelFrame(text="log", fg="green", bg="powderblue")
history_frame.place(relx=0, rely=0)
history = tk.Text(history_frame, width=60, height=18)
history.pack()
running = False


def existsone():
    return exists(os.path.join(installpath, "game.py"))


def choosepath():
    global installpath, button
    new_installpath = filedialog.askdirectory()
    if new_installpath == installpath or new_installpath == "":
        return
    installpath = new_installpath
    if existsone():
        button.config(text="立即更新")
    else:
        button.config(text="立即下载" if sc else "立即下載")


installlbl = tk.Label(updater)
installlbl.place(relx=0.025, rely=0.875)
installlbl.config(text=f"安装路径: {installpath}" if sc else f"安裝路徑: {installpath}")
choosebtn = tk.Button(
    updater, text="选择路径" if sc else "選擇路徑", command=choosepath
)
choosebtn.place(relx=0.875, rely=0.75)
button = tk.Button(updater, command=updategame)
button.place(relx=0.875, rely=0.5)
if existsone():
    button.config(text="立即更新")
else:
    button.config(text="立即下载" if sc else "立即下載")


def refresh():
    global installlbl
    installlbl.config(
        text=f"安装路径: {installpath}" if sc else f"安裝路徑: {installpath}"
    )
    updater.after(1000, refresh)


updater.after(0, refresh)

updater.mainloop()
