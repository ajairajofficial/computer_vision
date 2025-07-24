to delete the current environment :
open command prompt not powershell
rmdir /s /q venv 
/s means recursively subfolders /q means do it quietly without much prompts.


############################################################################################################################
create an env in the current folder 
get into cmd on ide terminal
conda create -p venv python==3.9       (create a new env in the current folder) -p says in current folder, venv is the name of the env
conda activate venv/

should come up like this: (venv) C:\Users\ajair\Desktop\github\AiSystemLabs\face_recognition_project or
(c:\Users\ajair\Desktop\github\AiSystemLabs\face_recognition_project\venv) C:\Users\ajair\Desktop\github\AiSystemLabs\face_recognition_project

conda install opencv numpy -c conda-forge
pip install face_recognition dlib
# inorder to install 

for excel output
pip install openpyxl

for google spreadsheet
pip install gspread google-auth
#############################################################################################################################

Also create a txt file inside the folder as requirements.txt and write all the packages needed. 
Then in terminal do pip install -r requirements.txt and it will install all in one go.
always make sure all the packages are installed inside the venv. but all the programs are created outside the venv.


run the python file in the terminal by using python filename.py
python face_recognition_app.py






some info
Why You Need dlib for face_recognition
The face_recognition Python library depends on dlib under the hood because it uses:
dlib's deep learning face embedding model
dlib's HOG-based face detector
dlib's face landmark predictor

dlib is a C++ library. When you install it via pip on Windows, it compiles from source using CMake
and a C++ compiler (like MSVC, which comes with Visual Studio Build Tools).
Windows doesn’t have a native C++ compiler available out of the box (unlike Linux/macOS). That’s why:
🛠️ You must have Visual Studio Build Tools installed on Windows to build C++ extensions like dlib.