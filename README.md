# Dog Breed Classification Web Application!

Frontend : React.js (https://dog-bleed-classification.netlify.app)

Backend : Flask

Demo video : https://drive.google.com/file/d/1BZGSqmgK2kHXNFoz5YvToSFUmD0jgRa7/view?usp=sharing

# Requirements

You need to install **Node.js**.

## Getting Started for Frontend

Install necessary dependencies for the frontend React.js and run the development server for frontend.
You can also use this deployed web for the frontend. 
URL: (https://dog-bleed-classification.netlify.app)

```bash
cd Frontend
npm install
# or
yarn install

# then run the frontend server
npm run dev

```

## Download datasets

```bash
!wget -q https://gitlab.com/atlonxp/siit-deep-learning/-/raw/main/dogImages.zip -O dogImages.zip

!wget -q https://gitlab.com/atlonxp/siit-deep-learning/-/raw/main/lfw.zip -O lfw.zip

!wget -q https://gitlab.com/atlonxp/siit-deep-learning/-/raw/main/DogXceptionData.npz -O bottleneck_features/DogXceptionData.npz

# Yolo

!wget "https://pjreddie.com/media/files/yolov3.weights"

!wget "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg"
```

# Unzip datasets

```bash
!unzip -qq dogImages.zip
!unzip -qq lfw.zip
!rm -rf __MACOSX/
```

## Getting Started for Backend

Install necessary dependencies for the backend Flask and run the development server for backend

```bash
cd Backend
pip install flask
pip install flask-cors
pip install tensorflow
pip install pillow
pip install opencv
pip install numpy
pip install tqdm

# then run the backend server
python server.py
```

## **Team and Contribution**

Pattarapol Wangnirun 6322770981

Boonyakorn Rathasamuth 6322771047

Kanyapat Thanee 6322771427

Theerawuth Udomponglukkana 6322772516

**Department of Information, Computer and Communication Technology (ICT), Sirindhorn International Institute of Technology (SIIT), Thammasat University, Khlong Luang, Pathum Thani, Thailand**
