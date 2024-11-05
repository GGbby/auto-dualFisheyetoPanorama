import subprocess
import cv2
import os
import time
import shutil
import threading
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 設定區域：統一管理程式中的參數變數
INPUT_DIRECTORY = "./fishcam_input/"           # 監控的輸入資料夾
OUTPUT_DIRECTORY = "./output_panorama/"         # 輸出的全景圖資料夾
CACHE_DIRECTORY = "./cache_LR/"                 # 暫存左右分割圖片的資料夾
PTO_TEMPLATE_PATH = "./hugin_ptofile/left_fisheye - right_fisheye.pto"  # 拼接模板 .pto 檔案路徑
EXIFTOOL_PATH = "exiftool"                      # exiftool 指令路徑
AUTOOPTIMISER_PATH = "autooptimiser"            # autooptimiser 指令路徑
NONA_PATH = "nona"                              # nona 指令路徑
ENBLEND_PATH = "enblend"                        # enblend 指令路徑

# 更新 .pto 文件中的圖像路徑
def update_pto_file(pto_path, left_image_path, right_image_path):
    """更新 .pto 檔案中的左右圖像路徑"""
    left_image_abs_path = os.path.abspath(left_image_path)
    right_image_abs_path = os.path.abspath(right_image_path)
    
    with open(pto_path, 'r') as file:
        lines = file.readlines()
    
    with open(pto_path, 'w') as file:
        for line in lines:
            if 'left_fisheye' in line:
                file.write(f'i w1520 h1520 f2 v210.627402248555 Ra-0.773880660533905 Rb0.282591789960861 Rc-0.900835752487183 Rd-1.23824727535248 Re-0.153675630688667 Eev0 Er1 Eb1 r-2.31258405110029 p-1.03949596925098 y-72.0770471505879 TrX0 TrY0 TrZ0 Tpy0 Tpp0 j0 a0 b0 c0 d-10.8024140499825 e8.93014033718215 g0 t0 Va1 Vb0 Vc0 Vd0 Vx0 Vy0  Vm5 n"{left_image_abs_path}"\n')
            elif 'right_fisheye' in line:
                file.write(f'i w1520 h1520 f2 v=0 Ra=0 Rb=0 Rc=0 Rd=0 Re=0 Eev0.257883560395677 Er1.04511628806482 Eb0.992191313822991 r0.261795904191419 p-0.0307309248772816 y105.981070489337 TrX0 TrY0 TrZ0 Tpy0 Tpp0 j0 a=0 b=0 c=0 d=0 e=0 g=0 t=0 Va=0 Vb=0 Vc=0 Vd=0 Vx=0 Vy=0  Vm5 n"{right_image_abs_path}"\n')
            else:
                file.write(line)

# 分割雙魚眼圖像
def split_fisheye_image(input_image_path, output_left_path, output_right_path):
    """將輸入的雙魚眼圖像分割成左右兩張圖片"""
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"無法載入圖像: {input_image_path}")
        return False
    
    height, width = image.shape[:2]
    
    # 分割為左右兩部分
    left_fisheye = image[:, :width // 2]
    right_fisheye = image[:, width // 2:]
    
    # 保存分割後的圖像
    cv2.imwrite(output_left_path, left_fisheye)
    cv2.imwrite(output_right_path, right_fisheye)
    print(f"圖像已成功分割並保存。\n左邊: {output_left_path}\n右邊: {output_right_path}")
    return True

# 使用模板生成全景圖
def create_panorama_with_template(left_image_path, right_image_path, output_prefix):
    """根據左右魚眼圖像及模板 .pto 檔案生成全景圖"""
    # 使用唯一名稱的 .pto 文件來避免覆蓋
    unique_suffix = str(int(time.time() * 1000))  # 毫秒級時間戳
    temp_pto_file = f"{output_prefix}_temp_{unique_suffix}.pto"
    
    # 複製模板 .pto 文件
    shutil.copyfile(PTO_TEMPLATE_PATH, temp_pto_file)
    
    # 更新 .pto 文件中的圖像路徑
    update_pto_file(temp_pto_file, left_image_path, right_image_path)
    
    # 自動優化對齊參數
    subprocess.run([AUTOOPTIMISER_PATH, "-a", "-l", "-s", "-m", "-o", temp_pto_file, temp_pto_file])
    
    # 使用 nona 生成投影的 .tif 圖片
    output_tif_base = f"{output_prefix}_pano_{unique_suffix}"
    subprocess.run([
        NONA_PATH,
        "-z", "LZW", "-r", "ldr", "-m", "TIFF_m",
        "-o", output_tif_base, temp_pto_file
    ])
    
    # 使用 enblend 融合 .tif 文件並生成最終全景圖
    output_tif_files = [f"{output_tif_base}0000.tif", f"{output_tif_base}0001.tif"]
    output_jpg_path = f"{output_prefix}.jpg"  # 使用固定的名稱格式，不添加 unique_suffix
    subprocess.run([
        ENBLEND_PATH,
        "--compression=90", "-w", "-o", output_jpg_path
    ] + output_tif_files)
    
    # 檢查是否生成了最終的 JPG 圖像
    if os.path.exists(output_jpg_path):
        print(f"全景圖像生成成功：{output_jpg_path}")
    else:
        print("未能成功生成全景圖像。")

    # 更新圖像的元數據（可選步驟）
    exif_file_path = left_image_path  # 使用左圖像的 EXIF 作為範本
    if os.path.exists(exif_file_path):
        subprocess.run([
            EXIFTOOL_PATH,
            "-overwrite_original_in_place",
            "-TagsFromFile", exif_file_path,
            output_jpg_path
        ])
        print("元數據已更新。")

    # 清理臨時文件
    for temp_file in output_tif_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    if os.path.exists(temp_pto_file):
        os.remove(temp_pto_file)

    # 清理左右分割的臨時圖片
    if os.path.exists(left_image_path):
        os.remove(left_image_path)
    if os.path.exists(right_image_path):
        os.remove(right_image_path)

# 文件監控處理程序
class ImageHandler(FileSystemEventHandler):
    """監控資料夾中的新圖像檔案，並將其加入佇列"""
    def __init__(self, queue):
        self.queue = queue

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"檢測到新圖像: {event.src_path}")
            self.queue.put(event.src_path)

# 處理圖像
def process_images(queue):
    """從佇列中取出圖像，進行分割與拼接"""
    while True:
        input_image_path = queue.get()
        if input_image_path is None:
            break
        base_name = os.path.splitext(os.path.basename(input_image_path))[0]
        output_left_path = os.path.join(CACHE_DIRECTORY, f"{base_name}_left_fisheye.jpg")
        output_right_path = os.path.join(CACHE_DIRECTORY, f"{base_name}_right_fisheye.jpg")
        output_prefix = os.path.join(OUTPUT_DIRECTORY, f"{base_name}_p")

        # 分割圖像
        if split_fisheye_image(input_image_path, output_left_path, output_right_path):
            # 使用模板文件進行拼接
            create_panorama_with_template(output_left_path, output_right_path, output_prefix)
        queue.task_done()

# 主程序
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    if not os.path.exists(CACHE_DIRECTORY):
        os.makedirs(CACHE_DIRECTORY)

    image_queue = Queue()

    # 預先將資料夾中現有的圖像加入佇列
    for filename in os.listdir(INPUT_DIRECTORY):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(OUTPUT_DIRECTORY, f"{base_name}_p.jpg")
            if not os.path.exists(output_path):
                image_queue.put(os.path.join(INPUT_DIRECTORY, filename))

    # 啟動圖像處理執行緒
    threading.Thread(target=process_images, args=(image_queue,), daemon=True).start()

    # 設置資料夾監控
    event_handler = ImageHandler(image_queue)
    observer = Observer()
    observer.schedule(event_handler, INPUT_DIRECTORY, recursive=False)
    observer.start()

    print(f"正在監控資料夾: {INPUT_DIRECTORY}，等待新圖像...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    image_queue.put(None)
