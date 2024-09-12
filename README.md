# Machineheads

## AUTOMATED ROAD DAMAGE DETECTION FOR INFRASTRUCTURE MAINTENANCE
			          MACHINE LEARNING TRACK-01

Team Members: Aryan Patil, Mohammad Arif, Shruti Vanka, Siddique Borkar
University: National Institute of Technology, Warangal.

Topic: Automated Road Damage Detection for Infrastructure Maintenance

### INTRODUCTION:

Manual inspection and maintenance of road conditions is a tedious task and requires tremendous manpower. However, availability of continuous CCTV monitoring allows for scope in improvement. 
	Our project aims to automate road damage detection using a deep neural network in an effort to improve efficiency of the process. We detect any form of road damage and classify it into one of ten categories such as Potholes and Alligator cracks. We employ the 8th version of YOLO (You Only Look Once) to train our model and utilize the data provided in annotations format. Starting off with image datasets as input, we aim to extend our code’s reach to video input, in both recorded and live formats.

#### PROJECT SUMMARY: 
	
Older Algorithms utilized selective search algorithms to reduce number of candidate region proposals to 2k per frame and introduced modifications to improve speed but their rigidity limited their accuracy. Our research hence led us to YOLO -version 8 (faster and more accurate than all previous versions) that converges its effort onto high probability parts of the image. This in turn allows for it to use a single Convolutional Network to predict bounding boxes. 
	
We compared the performance of our local CUDA environment running in tandem with an Nvidia geforce rtx 2060 GPU and a cloud-hosted Google Colab set up(providing free access to remote GPUs and TPUs) . Upon finding significant improvement between both environments, we opted the latter. Our model ran for 10 EPOCHS and spanned 20k images in its training tenure. The ultralytics library was imported to work on the same. 

We have included features to take live video stream as well as prerecorded videos as input for our model to provide real-time predictions.  Our front-end GUI (developed using a combination of HTML, CSS and JavaScript) enables users to take video input using their webcam to provide prerecorded input for the model. We also allow direct access to our system’s webcam. Our model is hence allowed to analyze the continuous media stream (video) and output a video with bounding boxes annotating the regions of probable road damage.
	However, our model has limitations. Due to lack of effective firmware, we were unable to train our model sufficiently in time for it to provide higher mean average precision. Despite our time constraint, the model shows promise with a hiking rate of detecting accurately.

## XML to text
So, for us to use YOLO, we cannot just work with the images and xml files which were given. 
The xml files had the following important information: - the category of damage like D00, D10 etc. which start with a ‘D’ followed by numbers (or even a 0w0), the values of x-minimum, x-maximum, y-minimum and y-maximum. 
But YOLO files have the format ‘<Category> <coordinates of center for both x and y in the range of 0-1> <height and width of the bounded box in range 0-1>
So, the first task was to convert the xml files to yolo format txt files. I used a python script (xml2yolo.py) to do the above. But there was a lookup table on the basis of which the text files were being made, I have made the changes according to the classification categories in the lookup table so it finds all the types we want. The lookup table is a dictionary in which we give each label D00, D10 a numeric key like 0, 1 which will be the classification that will be stored in the txt file at the beginning of each row. 
To use this properly, just save the python file ‘xml2yolo.py’ in the same folder as all the xml files. Then, just go to the code, and run it. It should start writing new txt files in the yolo format. 

But as I did not already know all the categories of damages, I made another python script (getClasses.py) by learning upon the previous .py file. I went through all the files and wherever I found the  name tag for the category, I stored it in a list for unique category of damages and from all the xml files, I was able to find 10 types of damages.

Once I knew these, I made the lookup table in the xml to yolo txt conversion file. Which again goes through every xml file, fetches the category name, references the lookup table dictionary, gives the category number for yolo txt. Then as the xml files also have height and width of the image, based on that and the x and y max and min coordinates, we derive the other attributes. In each yolo txt file, the no. of rows signifies how many damages were detected in that image. So, this means that if there are no damages, then the yolo txt file will be empty.

Once we got these files, we imported YOLO by using ultralytics. It seemed to be very simple to use. Our model uses yolov8n (Nano). We made a config.yaml file in which we kept the paths for the training, validation and the testing set. It also consists the name of classes. Once we use the model function, yolov8, by itself, takes an image from the path given, then it finds its corresponding same named yolo txt file from the labels folder. Then, trains on the basis of the classes. This first happens on the training set. Then it does the same for the validation set, for which, just like train set, the annotations are given.

## Link to Videos
[Click me](https://drive.google.com/drive/folders/1uyLuVr0s6fMYBu4QHxj2qLRpYwWhpyks)
 
## Examples
### Predicted
<img title="a title" alt="Alt text" src="/images/download (2).png">

### Original
<img title="a title" alt="Alt text" src="/images/download (1).png">

### Predicted
<img title="a title" alt="Alt text" src="/images/download (5).png">

### Original
<img title="a title" alt="Alt text" src="/images/download (6).png">

## How we trained our model
All the code in this section was run on google colab

### Dependencies
zipfile\
requests\
cv2\
matplotlib.pyplot\
glob\
random\
os\
torch with cuda\
ultralytics

### Folder Structure of dataset
	├── yolov8
	 ++ └── train
	 ++++└── images (folder including all training images)
	 ++++└── labels (folder including all training labels)
	 ++ └── test (optional)
	 ++++└── images (folder including all testing images)
	 ++ └── valid
	 ++++└── images (folder including all testing images)
	 ++++└── labels (folder including all testing labels)


### config.yaml
```
%%writefile pothole_v8.yaml
path: ''
train: 'train/images'
val: 'valid/images'

# class names
names:
    0: longitudinal_crack
    1: s1
    2: s2
    3: transverse_crack
    4: s3
    5: aligator_crack
    6: pothole
    7: s4
    8: s5
    9: s6

# class names
names:
  0: 'pothole'
```

### yolov8n training
```
EPOCHS = 5
!yolo task=detect mode=train model=yolov8n.pt imgsz=1280 data=config.yaml epochs={EPOCHS} batch=8 name=yolov8n_v8_50e
```

### To predict annotation on an image
```
from ultralytics import YOLO

# Load a model
model = YOLO('best.pt')  # YOLOv8n model trained by us

# Run batched inference on a list of images
results = model(['im1.jpg', 'im2.jpg'])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    result.show()  # display to screen
    result.save(filename='result.jpg') 

```

### To validate the model
```
!yolo task=detect mode=val model=runs/detect/yolov8n_v8_50e/weights/best.pt name=yolov8n_eval data=pothole_v8.yaml
```

## Evaluation of final model on validation data
<img title="a title" alt="Alt text" src="/images/valid.png">


## offline_pred.py
this file takes two video files (prerecorded) as input, runs the model on them concurrently using the threading library and gives the annotated videos as input. 
	To run on your system, change the video_file1 and videofile_2 paths to where your videos are stored and the model1, model2 paths to your .pt file locations (i.e. to where the pretrained models are stored). Press the q key to exit the live stream.
## real_time_pred.py
 this file uses the cv2 library to connect a path to the webcam of your system and obtain real-time data.
 	To run on your system, you only need to change the model's path to where your .pt file is stored.
  Press the q key to exit the live stream.


:)

