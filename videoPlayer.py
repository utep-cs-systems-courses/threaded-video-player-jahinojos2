#!/usr/bin/env python3

import cv2
import threading

from Queue import Queue

VIDEOFILE = "./clip.mp4"
DELIMETER = "\0"
FRAMEDELAY = 42


def extractFrames(fileName, queue):

    if fileName is None:
        raise TypeError
    if queue is None:
        raise TypeError

    video = cv2.VideoCapture(fileName)

    success, img = video.read()

    imgIndex = 0
    
    while success:
        queue.put(img)

        success, img = video.read()

        print(f'Frame {imgIndex} {success} processing')
        imgIndex += 1

    print('Frames have been extracted');

    queue.put(DELIMETER)

def convertGrayscale(colorFrames, grayFrames):

    if colorFrames is None:
        raise TypeError
    if grayFrames is None:
        raise TypeError

    imgIndex = 0

    colorFrame = colorFrames.get()

    while colorFrame is not DELIMETER:
        print(f'Converting frame {imgIndex}')

        grayFrame =cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
        grayFrames.put(grayFrame)
        imgIndex += 1
        colorFrame = colorFrames.get()

    print('Conversion to gray scale complete')
    grayFrames.put(DELIMETER)

def displayFrames(frames):
    if frames is None:
        raise TypeError

    index = 0

    frame = frames.get()

    while frame is not DELIMETER:
        print(f'Displaying frame {index}')

        cv2.imshow('Play', frame)

        if cv2.waitKey(FRAMEDELAY) and 0xff == ord("q"):
            break

        index += 1
        frame = frames.get()

    print('Frames displayed')
    cvw.destroyAllWindows()

if __name__ == "__main__":

    colorFrames = Queue()
    grayFrames = Queue()

    extractThread = threading.Thread(target = extractFrames, args = (VIDEOFILE, colorFrames))
    convertThread = threading.Thread(target = convertGrayscale, args=(colorFrames, grayFrames))
    displayThread = threading.Thread(target = displayFrames, args =(grayFrames,))

    extractThread.start()
    convertThread.start()
    displayThread.start()
        
    
        
