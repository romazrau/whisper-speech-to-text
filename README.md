# Whisper on Mac 音檔轉文字


## 準備基本環境
1. 確保已經安裝 Homebrew
2. 安裝 Python
    - Whisper 需要 Python 環境。[版本請參考 Whisper Github](https://github.com/openai/whisper?tab=readme-ov-file#setup)
    ```bash
    brew install python@3.11
    
    # 確認版本
    python3 --version
    
    # 選用，設定環境變數，使 Python 3.11 成為預設版本
    brew unlink python
    brew link python@3.11
    ```
    
3. 建立 Python 虛擬環境
    ```bash
    # mkdir && cd to your workspace
    cd ~/dev/whisper/
    
    # 建立虛擬環境
    python3.11 -m venv venv

    # 啟動虛擬環境
    source venv/bin/activate
    
    # 備用指令，離開虛擬環境
    deactivate
    ```

3. 安裝其他相依於 python 的套件
    
    - [安裝 PyTorch](https://pytorch.org/get-started/locally/)
    ```bash
    pip3 install torch torchvision torchaudio
    ```
    

4. 安裝 ffmpeg
    - ffmpeg 是處理音頻和視頻的工具，Whisper 依賴它來處理音頻文件。
    ```bash
    brew install ffmpeg
    ```
    
5. 安裝 Whisper
    ```bash
    pip install -U openai-whisper

    # 確認安裝成功
    whisper --help
    ```
    
## [Command-line usage](https://github.com/openai/whisper?tab=readme-ov-file#command-line-usage)
1. 找個檔案測試
    ```bash
    whisper 3012792063.mp3 --language Chinese --model medium
    ```
    結果：
    ![image](https://hackmd.io/_uploads/H13iBgEHyx.png)


## [Python usage](https://github.com/openai/whisper?tab=readme-ov-file#python-usage)
1. 新建檔案 template_loacl_transcribe.py
    ```python
	import whisper
	from datetime import datetime
	
	start = datetime.now()
	
	model = whisper.load_model("turbo")
	
	# load audio and pad/trim it to fit 30 seconds
	audio = whisper.load_audio("assets/Sonnet_18_William_Shakespeare.mp3")
	audio = whisper.pad_or_trim(audio)
	
	# make log-Mel spectrogram and move to the same device as the model
	mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
	
	# detect the spoken language
	_, probs = model.detect_language(mel)
	print(f"Detected language: {max(probs, key=probs.get)}")
	
	# decode the audio
	options = whisper.DecodingOptions()
	result = whisper.decode(model, mel, options)
	
	# print the recognized text
	print(result.text)
	
	end = datetime.now()
	difference = end - start
	print(f"Time spent: {difference}")
    ```
2. 測試
    ![image](https://hackmd.io/_uploads/BkhQ0XNByx.png)


## 使用 OpenAI API (需付費)
因為地端跑很慢，改用 OpenAI API 可以快很多。
1. [準備 API Key](https://platform.openai.com/docs/quickstart)
    - [Start building](https://platform.openai.com/docs/overview)
        ![image](https://hackmd.io/_uploads/rJ3ndQEr1x.png)
        - 新增付款方式，預設會是 Pay as you go，可一次儲值 5 美金
        - 記得設定 [Limits 管理使用與用量警告](https://platform.openai.com/settings/organization/limits)
        -  前往 https://platform.openai.com/api-keys 建立 API key
        -  將 API key 存進環境變數
            ```bash
            # ~/.zshrc
            # Export an environment variable on macOS
            export OPENAI_API_KEY="your_api_key_here"
            ```
        - close file and run:
            ```bash
            source ~/.zshrc
            ```

2. 安裝 OpenAI SDK
    ```bash
    pip install openai
    ```
    
3. 新建檔案 template_loacl_transcribe.py
	```python
	import os
	import openai
	from datetime import datetime
	
	start = datetime.now()
	
	openai.api_key = os.getenv("OPENAI_API_KEY")
	client = openai.OpenAI()
	
	audio_file = open("assets/Sonnet_18_William_Shakespeare.mp3", "rb")
	transcript = client.audio.transcriptions.create(
	    model="whisper-1",
	    file=audio_file
	)
	
	print(transcript.text)
	
	end = datetime.now()
	difference = end - start
	print(f"Time spent: {difference}")
	```

4. 測試
    ![image](https://hackmd.io/_uploads/SJ9qJE4Syx.png)

## 附錄
### 轉檔 m4a to mp3
```bash
shell_scripts/batch_convert.sh
```