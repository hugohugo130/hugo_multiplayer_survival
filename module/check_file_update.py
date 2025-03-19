def cfu():
    """
    檢查文件更新
    返回值：
    1: 有更新
    0: 沒有更新
    """
    from os.path import exists, getsize
    import tempfile
    import os
    import zipfile
    import shutil

    try:
        import gdown
    except ModuleNotFoundError:
        from subprocess import run
        from sys import executable

        run([executable, "-m", "pip", "install", "gdown"])
        import gdown

    # Google Drive 檔案ID
    gdrive_id = "1TK8O5OhxbUC29qHD2Qm1TId8bR37CmhX"
    
    # 建立臨時資料夾
    temp_dir = os.path.join(tempfile.gettempdir(), "game_temp_check")
    if exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    zip_path = os.path.join(temp_dir, "game_files.zip")
    extract_path = os.path.join(temp_dir, "extracted")
    if exists(extract_path):
        shutil.rmtree(extract_path)
    os.makedirs(extract_path)
    
    try:
        # 下載ZIP檔案
        gdown.download(
            f"https://drive.google.com/uc?id={gdrive_id}",
            zip_path,
            quiet=True
        )
        
        # 檢查下載的檔案是否有效
        if not exists(zip_path) or getsize(zip_path) < 1000:  # 如果檔案小於1KB
            return 0
            
        # 解壓縮檔案
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
            
        # 動態獲取所有.py檔案
        files_to_check = []
        ignore_dirs = ["__pycache__", "data", "output", "decrypt"]
        
        for root, dirs, files in os.walk(extract_path):
            # 移除要忽略的目錄
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file.endswith(".py"):
                    # 獲取相對路徑
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, extract_path)
                    files_to_check.append(rel_path)
        
        # 比較檔案
        for file_path in files_to_check:
            local_path = file_path
            remote_path = os.path.join(extract_path, file_path)
            
            # 如果本地檔案不存在，需要更新
            if not exists(local_path):
                return 1
                
            # 比較檔案內容
            with open(local_path, 'rb') as local_file, open(remote_path, 'rb') as remote_file:
                if local_file.read() != remote_file.read():
                    return 1  # 檔案內容不同，需要更新
        
        # 如果所有檔案都相同，不需要更新
        return 0
        
    except Exception as e:
        print(f"檢查更新時出錯: {e}")
        return 0
    finally:
        # 清理臨時檔案
        if exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    result = cfu()
    if result == 1:
        print("發現更新！")
    else:
        print("沒有更新。")
    input()
