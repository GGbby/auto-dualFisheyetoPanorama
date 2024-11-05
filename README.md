### Language：
- [English Version](README_en.md)
- [中文版](README.md)

# Panorama Image Processing Project

本專案用於自動處理雙魚眼圖像並生成全景拼接圖。當有新圖像加入監控資料夾時，程式會自動分割雙魚眼圖像並拼接成全景圖，最後輸出至指定的資料夾。

## 主要功能
- **雙魚眼圖像分割**：自動將雙魚眼圖像分為左右兩部分。
- **圖像拼接**：使用 Hugin 工具生成全景圖。
- **資料夾監控**：持續監控 `fishcam_input/` 資料夾，並自動處理新加入的圖像。

## 專案結構
```
│  .gitattributes 
│  main.py
│  README.md
│  requirements.txt
│
├─cache_LR
├─fishcam_input
│       // dual fisheye image
│
├─hugin_ptofile
│      left_fisheye - right_fisheye.pto  //demo內容
│
└─output_panorama
        // 360 panorama image
```
        
- **`main.py`**：主程式，負責監控資料夾中的圖像，分割雙魚眼圖像並生成全景圖。
- **`cache_LR/`**：暫存分割的左右圖像。
- **`fishcam_input/`**：存放待處理的雙魚眼圖像。
- **`hugin_ptofile/`**：存放 Hugin 拼接模板文件（.pto）。
- **`output_panorama/`**：輸出生成的全景圖。

## 依賴需求

本專案依賴以下 Python 套件及外部工具：

### Python 套件
請先安裝 Python 套件。可以使用以下指令安裝 `requirements.txt` 中的依賴：
```bash
pip install -r requirements.txt
```

### 外部工具
以下能容是在製作時使用的工具，不確定若只是運行的話是否需要，Hugin應該需要，用於圖像拼接及元數據處理：

- Hugin 工具套件：包括 autooptimiser、nona、enblend 等指令。我個人在開發時是在windows使用Hugin GUI的完整內容在製作的。
- ExifTool：用於更新輸出圖像的元數據。

### 使用方法
- ```pip install -r requirements.txt```
- 使用環境：
  - python 3.11.7 (in conda //不影響)
  - no other else
- 確認你的```.pto```檔以及**fisheye_image**存在且路徑正確
- 單純運行```main.py```
- 有需要注意main.py的開頭的文件位置，有用備註標示每個辨識分別是什麼，請注意directory的位置以及.pto的位置宣告是否正確
