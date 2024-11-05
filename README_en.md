### Language:
- [English Version](README_en.md)
- [中文版](README.md)

# Panorama Image Processing Project

This project is designed to automatically process dual-fisheye images and generate stitched panoramic images. When new images are added to the monitored folder, the program will automatically split the dual-fisheye images and stitch them into panoramic images, saving the output to a designated folder.

## Key Features
- **Dual-Fisheye Image Splitting**: Automatically splits dual-fisheye images into left and right parts.
- **Image Stitching**: Utilizes Hugin tools to generate panoramic images.
- **Folder Monitoring**: Continuously monitors the `fishcam_input/` folder and processes newly added images.

## Project Structure
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

- **`main.py`**: Main script that monitors the folder for images, splits dual-fisheye images, and generates panoramic images.
- **`cache_LR/`**: Temporarily stores the split left and right images.
- **`fishcam_input/`**: Stores dual-fisheye images to be processed.
- **`hugin_ptofile/`**: Stores the Hugin stitching template file (.pto).
- **`output_panorama/`**: Stores the generated panoramic images.

## Requirements

This project depends on the following Python packages and external tools:

### Python Packages
Install the required Python packages by running:
```bash
pip install -r requirements.txt
```

### External Tools
The following tools were used during development. For simply running the program, only Hugin may be required, depending on your environment:

- Hugin Tool Suite: Includes commands like autooptimiser, nona, and enblend. Hugin is the primary tool for stitching, and it's recommended to install the complete GUI version to ensure all commands are available.
- ExifTool: Used to update metadata of the output images.
### Usage introduction
- ```pip install -r requirements.txt```
- Environment:
  - Python 3.11.7 (using conda is optional and doesn't affect functionality)
  - No other requirements
- make sure your```.pto```and the fisheye images' location information is correct
- Run main.py

> *** Note: At the beginning of main.py, there are variables to specify directory paths and the location of the .pto file. Please verify that the directory paths and the .pto template file are correctly specified.***