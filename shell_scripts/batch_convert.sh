#!/bin/bash

# 獲取腳本檔案所在的目錄
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# 指定目標資料夾，使用腳本所在路徑的相對路徑 "../assets"
SOURCE_DIR="$SCRIPT_DIR/../assets"

# 切換到目標資料夾
cd "$SOURCE_DIR" || { echo "無法進入目標資料夾：$SOURCE_DIR"; exit 1; }

# 切換到目標資料夾
cd "$SOURCE_DIR"

# 批次轉換 .m4a 檔案為 .mp3
for file in *.m4a; do
  # 檢查檔案是否存在
  if [ -f "$file" ]; then
    echo "正在轉換 $file ..."
    ffmpeg -i "$file" -codec:a libmp3lame -q:a 2 "${file%.m4a}.mp3"
    echo "$file 已完成！"
  fi
done

# 詢問是否刪除 .m4a 檔案
read -p "是否要刪除所有 .m4a 檔案？(y/n): " delete_choice
if [[ "$delete_choice" == "y" || "$delete_choice" == "Y" ]]; then
  for file in *.m4a; do
    if [ -f "$file" ]; then
      rm "$file"
      echo "$file 已刪除。"
    fi
  done
  echo "所有 .m4a 檔案已刪除！"
else
  echo "保留 .m4a 檔案，未進行刪除。"
fi

echo "所有操作完成！"