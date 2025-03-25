# import libraries,
import cv2
import time 
import numpy

# prepare a blank image for failed videocapture
blank_image = numpy.zeros((500,500,3), numpy.uint8)

ImageFolderPath='CasClas/tsniff for pigeons' #testing from training data
CascadeClassifierPath='CasClas/pigeonClassifier/pigeon 6.xml'

# set sidplay parameters
fontSize=1
fontThick=2
fontType=cv2.FONT_HERSHEY_SIMPLEX
Color=(0,255,0)
resizeWeight=1

# IP webcam setup
User='webcam'
Password='webcam123'

# connect to IP webcam
# vidcap = cv2.VideoCapture('http://webcam:webcam123@192.168.1.9:8080/video')
# print('webcam connected')

# connect to local webcam
vidcap = cv2.VideoCapture(0)
print('webcam connected')

# time measuring function
def grab_time():
    return round(time.time()*1000) #[ms]

# frame capture function
def grab_frame():
    if vidcap.isOpened:                 # if the camera is accessible
        ret, frame = vidcap.read()      # define confirmation and frame of videocapture
        if ret:                         # if the capture is successfull
            return frame                # return the image
        else:                           # if the capture is unsucsessfull 
            print('Unable to capture frame')
            return blank_image          # return a blank image
    else:                               # if the camera is unaccessible
        print('Unable to open camera')
        return blank_image              # return a blank image

# search function
def sniff_for_pigeons(CapturedFrame,deltaT):
    minsize=[64,64]                                     # define minimum image size
    scent=cv2.CascadeClassifier(CascadeClassifierPath)  # define cascade classifier
    img=CapturedFrame                                   # define image to be processed
    imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)       # turn the image into grayscale
    found = scent.detectMultiScale(imgGray,minSize =(minsize[0], minsize[1])) # match the image properties with our cascade classifier
    amountFound = len(found)                            # define the amount of valid objects found
    if amountFound!=0:                                  # if there are valid objects present
        for (x,y,width,height) in found:                # iterate trough valid objects
            cv2.rectangle(img, (x, y), (x + height, y + width), Color, fontThick)                                       # draw a rectangle around valid object
            cv2.putText(img,(" x:"+str(x)+" y:"+str(y)),(x + height, y + width),fontType,fontSize,Color,fontThick)      # display the coordinates of valid objects
    cv2.putText(img, ("fps: "+str(round(1000/deltaT))), (100, img.shape[0] - 150), fontType,fontSize,Color,fontThick)   # display fps from elapsed time since the last image processed
    cv2.putText(img,("Pigeons found: "+str(amountFound)),(100, img.shape[0] - 100),fontType,fontSize,Color,fontThick)   # display the amount of valid objects found
    img = cv2.resize(img, (round(img.shape[1]/resizeWeight), round(img.shape[0]/resizeWeight)))                         # resize the processed image to a valid size (necesarry for cv2)
    return img                                          # return the processed image to be displayed

# prepare runtime variables
print('press q to exit')
dt=1                    # define an initial delta time to prevent division by zero
timeoutTrigger=3000     # define a timeout trigger in milliseconds 

# main loop
while(True):
    start=grab_time()                                       # measure time before image processing
    cv2.imshow("Frame",sniff_for_pigeons(grab_frame(),dt))  # process and display image
    end=grab_time()                                         # mesaure time after image proceesing
    dt=end-start                                            # calculate elapsed time
    if cv2.waitKey(1) & 0xFF == ord('q'):                   # exit main loop if user inout is "q" (quit)
        print("shutting down")
        break
    if dt>=timeoutTrigger:                                  # exit main loop if the process is taking longer than the specified timeout trigger
        print("timeout error loop completed over "+timeoutTrigger+"ms")
        break