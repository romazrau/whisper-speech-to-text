import os

def select_file(directory: str, extension: str = ".mp3") -> str:
    """
    列出指定目錄中的檔案，讓使用者選擇檔案返回其路徑。

    :param directory: 檔案目錄路徑。
    :param extension: 要篩選的檔案副檔名（預設為 .mp3）。
    :return: 使用者選擇的檔案完整路徑。
    """
    # 確保目錄存在
    if not os.path.exists(directory):
        raise FileNotFoundError(f"資料夾不存在：{directory}")

    # 列出目錄中符合副檔名的檔案
    files = [f for f in os.listdir(directory) if f.endswith(extension)]

    # 如果目錄中沒有符合條件的檔案
    if not files:
        raise FileNotFoundError(f"目錄 {directory} 中沒有找到任何 {extension} 檔案。")

    # 列出檔案並附上編號
    print(f"以下是 {directory} 中的可用檔案：")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    # 詢問使用者選擇檔案
    user_input = input("請輸入檔案編號或完整檔名：").strip()

    # 根據輸入決定檔案名稱
    if user_input.isdigit():  # 如果輸入的是數字編號
        file_index = int(user_input) - 1
        if 0 <= file_index < len(files):
            selected_file = files[file_index]
        else:
            raise ValueError("輸入的編號無效。")
    else:  # 如果輸入的是完整檔名
        if user_input in files:
            selected_file = user_input
        else:
            raise ValueError("輸入的檔名無效。")

    # 返回完整檔案路徑
    return os.path.join(directory, selected_file)