import cv2
import sys
import os
import logging as log
import datetime as dt
from time import sleep
import time
import click
import platform


def get_lock_screen_cmd():
    cmd_dict = {
        'Linux' : 'gnome-screensaver-command --lock &',
        'Darwin': '/System/Library/CoreServices/Menu\ Extras/user.menu/Contents/Resources/CGSession -suspend'
    }
    os_type = platform.system()
    if os_type in cmd_dict:
        return cmd_dict[os_type]
    else:
        raise Exception('Unsupported OS platform, Linux and MacOS only.')


@click.command()
@click.option('--delay-seconds', help='activate command after this many seconds without detecting a face', default=5)
@click.option('--sleep-seconds', help='sleep every this many seconds', default=0.5)
def run(delay_seconds, sleep_seconds):
    # cascPath = "/home/wei/dev/facelock/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    log.basicConfig(filename='webcam.log',level=log.INFO)

    video_capture = cv2.VideoCapture(0)
    anterior = 0
    counter = 0
    TRIGGER = int(sleep_seconds * delay_seconds)
    # fps = video_capture.get(cv2.CAP_PROP_FPS) # Gets the frames per second
    # multiplier = fps * seconds

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(3)
            pass

        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len (faces) < 1:
            counter += 1
            log.info("no face at "+str(dt.datetime.now()) + ' counter='+ str(counter))

            if counter > TRIGGER:

                os.popen(get_lock_screen_cmd())
                # video_capture.release()
                # cv2.destroyAllWindows()
                # break

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if anterior != len(faces):
            anterior = len(faces)
            # log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
            counter = 0

        # Display the resulting frame
        cv2.imshow('Face Detection', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Display the resulting frame
        #cv2.imshow('Video', frame)
        time.sleep(sleep_seconds) # Sleep for x second
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()