to delete the current environment :
open command prompt not powershell
rmdir /s /q venv 
/s means recursively subfolders /q means do it quietly without much prompts.


############################################################################################################################
create an env in the current folder 
get into cmd on ide terminal
conda create -p venv python==3.9       (create a new env in the current folder) -p says in current folder, venv is the name of the env

to activate the newly created environment
conda activate venv/

should come up like this: 
(C:\Users\ajair\Desktop\github\computer_vision\Barcode_Scanner\venv) C:\Users\ajair\Desktop\github\computer_vision\Barcode_Scanner>


now install the packages
package lists are saved in the requirements.txt

then  

pip install -r requirements.txt



#############requirement list#########################

# Stable PyTorch CPU version for Windows

torch==2.2.0
torchvision==0.17.0
torchaudio==2.2.0

# Computer Vision
opencv-python
opencv-contrib-python

# Barcode reading support
pyzbar

# YOLOv5 - maintained by Ultralytics
ultralytics

# Plotting and training tools
matplotlib
seaborn
pandas
tqdm

# For labeling images (manual annotation)
labelImg





create a folder structure like this 

your_project_directory/
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   ├── labels/
│   │   ├── train/
│   │   └── val/


once you are in the project directory (cmd)
try this to create a folder structure.(YOLOv5- compatible) 

mkdir dataset
mkdir dataset\images
mkdir dataset\images\train
mkdir dataset\images\val
mkdir dataset\labels
mkdir dataset\labels\train
mkdir dataset\labels\val


########################################################################

You do NOT need to train the barcode-to-integer logic — the decoding part (i.e., turning a barcode image into a number) 
is already handled by existing barcode libraries like pyzbar, opencv, or ZBar.

You only need to train the YOLO model to detect the location of the barcode reliably under harsh conditions (blur, glare, angle, etc.).

#######################################################################

Full Flow of Your System:
#################################################################################################################################
1. YOLOv5: Barcode Detection (Your Training Focus)
Input: Live camera feed from Jetson Nano
Output: Bounding box around the barcode

Your model says:

“There’s a barcode in this region — crop it.”

2. Barcode Decoder (No Training Needed)
Use pyzbar, opencv, or zxing to decode the cropped image

Output: The barcode number as a string, e.g., "2415400017"

These libraries already know:
How to read EAN-13, Code 128, QR, etc.


No training is needed for that

You Train for These Use Cases:
Barcode is blurred
Covered with plastic
At extreme angles
In dark or reflective lighting
Only half-visible
Placed diagonally or sideways
Small in size or far from the camera
Your trained model must say:
“Even though it’s a mess, I still see a barcode there. Here's the box.”

Then the decoder will do its job.

#################################################################################################################################

labeling your barcode images using a tool like Roboflow or LabelImg



