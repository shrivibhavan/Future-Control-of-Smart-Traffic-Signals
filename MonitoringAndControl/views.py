from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
import cv2 as cv
import numpy as np
from ultralytics import YOLO
import datetime
from django.http import StreamingHttpResponse
import threading
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

model = YOLO("yolo11n.pt")
ann = keras.models.load_model("nn.keras")

#cam = cv.VideoCapture(0)
token = 1

data = {'noOfVehiclesWest':0,
        'noOfCarsWest':0,
        'noOfBikesWest':0,
        'noOfTrucksWest':0,
        'timerWest':0,
        'estimatedWaitTimeWest':0,

        'noOfVehiclesNorth':0,
        'noOfCarsNorth':0,
        'noOfBikesNorth':0,
        'noOfTrucksNorth':0,
        'timerNorth':0,
        'estimatedWaitTimeNorth':0,

        'noOfVehiclesSouth':0,
        'noOfCarsSouth':0,
        'noOfBikesSouth':0,
        'noOfTrucksSouth':0,
        'timerSouth':0,
        'estimatedWaitTimeSouth':0,

        'noOfVehiclesEast':0, 
        'noOfCarsEast':0,
        'noOfBikesEast':0,
        'noOfTrucksEast':0,  
        'timerEast':0, 
        'estimatedWaitTimeEast':0,    
}

timeTemp = datetime.datetime.now() + datetime.timedelta(0,2,0)

def detectVehicleSouth():
    global model
    frame = cv.imread('trafficTest4.jpeg')
    results = model(frame)
    
    for r in results:
        numberOfVehicles = 0
        numberOfCars = 0
        numberOfBikes = 0
        numberOfTrucks = 0
        boxes = r.boxes
        boxTensor = r.boxes.xyxy
        boxArray = boxTensor.cpu().numpy()
        for i in range(len(boxes)):
            if boxes[i].cls == 2:
                numberOfCars += 1
            elif boxes[i].cls == 3:
                numberOfBikes += 1
            elif boxes[i].cls == 7 or boxes[i].cls == 5:
                numberOfTrucks += 1
            else:
                continue
            numberOfVehicles += 1
    data['noOfVehiclesSouth'] = numberOfVehicles
    data['noOfCarsSouth'] = numberOfCars
    data['noOfBikesSouth'] = numberOfBikes
    data['noOfTrucksSouth'] = numberOfTrucks
    time.sleep(5)
    detectVehicleSouth()


def detectVehicleNorth():
    global model
    
    frame = cv.imread('trafficTest2.jpeg')
    results = model(frame)
    
    for r in results:
        numberOfVehicles = 0
        numberOfCars = 0
        numberOfBikes = 0
        numberOfTrucks = 0
        boxes = r.boxes
        boxTensor = r.boxes.xyxy
        boxArray = boxTensor.cpu().numpy()
        for i in range(len(boxes)):
            if boxes[i].cls == 2:
                numberOfCars += 1
            elif boxes[i].cls == 3:
                numberOfBikes += 1
            elif boxes[i].cls == 7 or boxes[i].cls == 5:
                numberOfTrucks += 1
            else:
                continue
            numberOfVehicles += 1
    data['noOfVehiclesNorth'] = numberOfVehicles
    data['noOfCarsNorth'] = numberOfCars
    data['noOfBikesNorth'] = numberOfBikes
    data['noOfTrucksNorth'] = numberOfTrucks
    time.sleep(5)
    detectVehicleNorth()



def detectVehicleWest():
    global model
    
    frame = cv.imread('trafficTest.jpeg')
    results = model(frame)
    for r in results:
        numberOfVehicles = 0
        numberOfCars = 0
        numberOfBikes = 0
        numberOfTrucks = 0
        boxes = r.boxes
        boxTensor = r.boxes.xyxy
        boxArray = boxTensor.cpu().numpy()
        for i in range(len(boxes)):
            if boxes[i].cls == 2:
                numberOfCars += 1
            elif boxes[i].cls == 3:
                numberOfBikes += 1
            elif boxes[i].cls == 7 or boxes[i].cls == 5:
                numberOfTrucks += 1
            else:
                continue
            numberOfVehicles += 1
    data['noOfVehiclesWest'] = numberOfVehicles
    data['noOfCarsWest'] = numberOfCars
    data['noOfBikesWest'] = numberOfBikes
    data['noOfTrucksWest'] = numberOfTrucks
    
    time.sleep(5)
    detectVehicleWest()

def detectVehicleEast():
    global model
    
    frame = cv.imread('trafficTest3.jpeg')
    results = model(frame)
    for r in results:
        numberOfVehicles = 0
        numberOfCars = 0
        numberOfBikes = 0
        numberOfTrucks = 0
        boxes = r.boxes
        boxTensor = r.boxes.xyxy
        boxArray = boxTensor.cpu().numpy()
        for i in range(len(boxes)):
            if boxes[i].cls == 2:
                numberOfCars += 1
            elif boxes[i].cls == 3:
                numberOfBikes += 1
            elif boxes[i].cls == 7 or boxes[i].cls == 5:
                numberOfTrucks += 1
            else:
                continue
            numberOfVehicles += 1
    data['noOfVehiclesEast'] = numberOfVehicles
    data['noOfCarsEast'] = numberOfCars
    data['noOfBikesEast'] = numberOfBikes
    data['noOfTrucksEast'] = numberOfTrucks
    time.sleep(5)
    detectVehicleEast()

f5 = threading.Thread(target=detectVehicleWest)
f2 = threading.Thread(target=detectVehicleEast)
f3 = threading.Thread(target=detectVehicleSouth)
f4 = threading.Thread(target=detectVehicleNorth)

f5.start()
f2.start()
f3.start()
f4.start()


def homepage(request):
    template = loader.get_template('homepage.html')
    context = {
        'noOfVehiclesWest':0,
        'noOfVehiclesNorth':0,
        'noOfVehiclesSouth':0,
        'noOfVehiclesEast':0,
    }
    return HttpResponse(template.render(context,request))

def calculateEstimatedWaitTime():
    if token == 2: #2 is North
        prediction = ann.predict(
            np.array(
                [[data['noOfCarsEast'],data['noOfBikesEast'],data['noOfTrucksEast']],
                [data['noOfCarsSouth'],data['noOfBikesSouth'],data['noOfTrucksSouth']]]
            ),
        )
        data['estimatedWaitTimeWest'] = (timeTemp+datetime.timedelta(0,int(prediction[0])+int(prediction[1]),0)-datetime.datetime.now()).seconds
        data['estimatedWaitTimeNorth'] = 0
        data['estimatedWaitTimeEast'] = (timeTemp-datetime.datetime.now()).seconds
        data['estimatedWaitTimeSouth'] = (timeTemp+datetime.timedelta(0,int(prediction[0]),0)-datetime.datetime.now()).seconds
    elif token == 3: #3 is East
        prediction = ann.predict(
            np.array(
                [[data['noOfCarsSouth'],data['noOfBikesSouth'],data['noOfTrucksSouth']],    
                [data['noOfCarsWest'],data['noOfBikesWest'],data['noOfTrucksWest']]]
            ),
        )
        data['estimatedWaitTimeWest'] = (timeTemp+datetime.timedelta(0,int(prediction[0]),0)-datetime.datetime.now()).seconds
        data['estimatedWaitTimeNorth'] = (timeTemp+datetime.timedelta(0,int(prediction[0])+int(prediction[1]),0)-datetime.datetime.now()).seconds
        data['estimatedWaitTimeEast'] = 0
        data['estimatedWaitTimeSouth'] = (timeTemp-datetime.datetime.now()).seconds
    elif token == 4: #4 is South
        prediction = ann.predict(
            np.array(
                [[data['noOfCarsWest'],data['noOfBikesWest'],data['noOfTrucksWest']],
                [data['noOfCarsNorth'],data['noOfBikesNorth'],data['noOfTrucksNorth']]]
            ),
        )
        data['estimatedWaitTimeWest'] = (timeTemp-datetime.datetime.now()).seconds
        data['estimatedWaitTimeNorth'] = (timeTemp+datetime.timedelta(0,int(prediction[0]),0)-datetime.datetime.now()).seconds
        data['estimatedWaitTimeEast'] = (timeTemp+datetime.timedelta(0,int(prediction[0])+int(prediction[1]),0)-datetime.datetime.now()).seconds
        data['estimatedWaitTimeSouth'] = 0
    elif token == 1: #1 is West
        prediction = ann.predict(
            np.array(
                [[data['noOfCarsNorth'],data['noOfBikesNorth'],data['noOfTrucksNorth']],
                [data['noOfCarsEast'],data['noOfBikesEast'],data['noOfTrucksEast']]]
            ),
        )
        data['estimatedWaitTimeWest'] = 0
        data['estimatedWaitTimeNorth'] = (timeTemp-datetime.datetime.now()).seconds
        data['estimatedWaitTimeEast'] = (timeTemp+datetime.timedelta(0,int(prediction[0]),0)-datetime.datetime.now()).seconds
        data['estimatedWaitTimeSouth'] = (timeTemp+datetime.timedelta(0,int(prediction[0])+int(prediction[1]),0)-datetime.datetime.now()).seconds

def getData(request):
    global token,timeTemp
    if(token == 1 and data['timerWest'] == 0):
        token = 2
        prediction = ann.predict(np.array([[data['noOfCarsNorth'],data['noOfBikesNorth'],data['noOfTrucksNorth']]])) #
        timeAlloted = int(prediction[0]) #
        if(timeAlloted<15):
            timeAlloted = 15
        #data['noOfVehiclesNorth'] = numberOfVehicles
        timeTemp += datetime.timedelta(0,timeAlloted,0)
        difference = timeTemp - datetime.datetime.now()
        data['timerNorth'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data)
    elif(token ==2 and data['timerNorth']!=0):
        difference = timeTemp - datetime.datetime.now()
        data['timerNorth'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data) 
    elif(token == 2 and data['timerNorth'] == 0):
        token = 3
        prediction = ann.predict(np.array([[data['noOfCarsEast'],data['noOfBikesEast'],data['noOfTrucksEast']]])) #
        timeAlloted = int(prediction[0]) #
        if(timeAlloted<15):
            timeAlloted = 15
        timeTemp += datetime.timedelta(0,timeAlloted,0)
        difference = timeTemp - datetime.datetime.now()
        data['timerEast'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data)
    elif(token == 3 and data['timerEast']!=0):
        difference = timeTemp - datetime.datetime.now()
        data['timerEast'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data)
    elif(token == 3 and data['timerEast']==0):
        token = 4
        prediction = ann.predict(np.array([[data['noOfCarsSouth'],data['noOfBikesSouth'],data['noOfTrucksSouth']]])) #
        timeAlloted = int(prediction[0]) #
        if(timeAlloted<15):
            timeAlloted = 15
        
        timeTemp += datetime.timedelta(0,timeAlloted,0)
        difference = timeTemp - datetime.datetime.now()
        data['timerSouth'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data)
    elif(token == 4 and data['timerSouth']!=0):
        difference = timeTemp - datetime.datetime.now()
        data['timerSouth'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data)
    elif(token == 4 and data['timerSouth'] == 0):
        token = 1
        prediction = ann.predict(np.array([[data['noOfCarsWest'],data['noOfBikesWest'],data['noOfTrucksWest']]])) #
        timeAlloted = int(prediction[0]) #
        if(timeAlloted<15):
            timeAlloted = 15
        timeTemp += datetime.timedelta(0,timeAlloted,0)
        difference = timeTemp - datetime.datetime.now()
        data['timerWest'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data)
    elif(token == 1 and data['timerWest']!=0):
        difference = timeTemp - datetime.datetime.now()
        data['timerWest'] = difference.seconds
        calculateEstimatedWaitTime()
        return JsonResponse(data)
    return JsonResponse(data)

def getDisplayData(request):
    return JsonResponse(data)

def displayWest(request):
    template = loader.get_template('display_west.html')
    return HttpResponse(template.render())


def vidStreamWest():
    #frame = cv.imread('trafficTest2.jpeg')
    while True:
        frame = cv.imread('trafficTest2.jpeg')
        results = model(frame)
        for r in results:
            boxes = r.boxes
            boxTensor = r.boxes.xyxy
            boxArray = boxTensor.cpu().numpy()
            for i in range(len(boxes)):
                if boxes[i].cls == 2: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(255,0,0),2)
                elif boxes[i].cls == 3: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,255,0),2)
                elif boxes[i].cls == 7 or boxes[i].cls == 5: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,0,255),2)
                else:
                    continue
        image_bytes = cv.imencode('.jpg',frame)[1].tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
        
def videoFeedWest(request):
    return StreamingHttpResponse(vidStreamWest(),content_type = 'multipart/x-mixed-replace; boundary=frame')

def displayEast(request):
    template = loader.get_template('display_east.html')
    return HttpResponse(template.render())

def vidStreamEast():
    #frame = cv.imread('trafficTest2.jpeg')
    while True:
        frame = cv.imread('trafficTest.jpeg')
        results = model(frame)
        for r in results:
            boxes = r.boxes
            boxTensor = r.boxes.xyxy
            boxArray = boxTensor.cpu().numpy()
            for i in range(len(boxes)):
                if boxes[i].cls == 2: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(255,0,0),2)
                elif boxes[i].cls == 3: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,255,0),2)
                elif boxes[i].cls == 7 or boxes[i].cls == 5: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,0,255),2)
                else:
                    continue
        image_bytes = cv.imencode('.jpg',frame)[1].tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
        
def videoFeedEast(request):
    return StreamingHttpResponse(vidStreamEast(),content_type = 'multipart/x-mixed-replace; boundary=frame')


def displayNorth(request):
    template = loader.get_template('display_north.html')
    return HttpResponse(template.render())

def vidStreamNorth():
    #frame = cv.imread('trafficTest2.jpeg')
    while True:
        frame = cv.imread('trafficTest3.jpeg')
        results = model(frame)
        for r in results:
            boxes = r.boxes
            boxTensor = r.boxes.xyxy
            boxArray = boxTensor.cpu().numpy()
            for i in range(len(boxes)):
                if boxes[i].cls == 2: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(255,0,0),2)
                elif boxes[i].cls == 3: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,255,0),2)
                elif boxes[i].cls == 7 or boxes[i].cls == 5: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,0,255),2)
                else:
                    continue
        image_bytes = cv.imencode('.jpg',frame)[1].tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
        
def videoFeedNorth(request):
    return StreamingHttpResponse(vidStreamNorth(),content_type = 'multipart/x-mixed-replace; boundary=frame')


def displaySouth(request):
    template = loader.get_template('display_south.html')
    return HttpResponse(template.render())

def vidStreamSouth():
    #frame = cv.imread('trafficTest2.jpeg')
    while True:
        frame = cv.imread('trafficTest5.jpeg')
        results = model(frame)
        for r in results:
            boxes = r.boxes
            boxTensor = r.boxes.xyxy
            boxArray = boxTensor.cpu().numpy()
            for i in range(len(boxes)):
                if boxes[i].cls == 2: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(255,0,0),2)
                elif boxes[i].cls == 3: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,255,0),2)
                elif boxes[i].cls == 7 or boxes[i].cls == 5: 
                    frame = cv.rectangle(frame, (int(boxArray[i][0]),int(boxArray[i][1])),(int(boxArray[i][2]),int(boxArray[i][3])),(0,0,255),2)
                else:
                    continue
        image_bytes = cv.imencode('.jpg',frame)[1].tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
        
def videoFeedSouth(request):
    return StreamingHttpResponse(vidStreamSouth(),content_type = 'multipart/x-mixed-replace; boundary=frame')