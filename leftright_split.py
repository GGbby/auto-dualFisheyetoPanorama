from PIL import Image

def split_fisheye_image(image_path, output_left_path, output_right_path):
    # 開啟影像
    image = Image.open(image_path)
    width, height = image.size
    
    # 計算左右部分的範圍
    left_box = (0, 0, width // 2, height)  # 左邊部分
    right_box = (width // 2, 0, width, height)  # 右邊部分
    
    # 裁切左右兩部分
    left_image = image.crop(left_box)
    right_image = image.crop(right_box)
    
    # 保存左右影像
    left_image.save(output_left_path)
    right_image.save(output_right_path)
    
    print("左右魚眼畫面已分割並保存：")
    print("左邊圖像路徑：", output_left_path)
    print("右邊圖像路徑：", output_right_path)

# 使用範例
input_image_path = './fishimage/15_2.jpg'  # 請根據您的檔案路徑調整
output_left_image_path = './fishimage/fishcam1_left_fisheye.jpg'
output_right_image_path = './fishimage/fishcam1_right_fisheye.jpg'

split_fisheye_image(input_image_path, output_left_image_path, output_right_image_path)
