# motion detector stuff
from gpiozero import MotionSensor
import time
import datetime
import picamera
import os
import shutil
from scp_send import pi_scp_send as ps
import argparse

parser = argparse.ArgumentParser(description="start up the PIR sensor")
parser.add_argument("username", help="enter the from email address", type=str)
parser.add_argument("remote_host", help="enter the to email address", type=str)
parser.add_argument("remote_dir", help="enter the remote directory", type=str)
args = parser.parse_args()

class pyTrigger:

    def __init__(self, username, hostname, remote_dir, port=22, m=4):
        self.username = username
        self.hostname = hostname
        self.remote_dir = remote_dir
        self.port = port
        self.motionsense = m
        self.pir = MotionSensor(self.motionsense)
        self.camera = picamera.PiCamera()

    def getFileName(self):
        return datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.jpg")

    def cameraCapture(self, file_path="."):
        # waiting for motion
        self.pir.wait_for_motion()
        if self.pir.motion_detected:
            # text to print for good feelings
            print("PIR Sensor Triggered!")
            # set file name now that detection has happened
            filename = self.getFileName()
            # these steps for picamera
            self.camera.resolution = (2592, 1944)
            # for debugging
            # camera.start_preview()
            time.sleep(0.1)
            fullpath = f"{file_path}/{filename}"
            self.camera.capture(fullpath)
            print(f"Image saved {fullpath}")
            return fullpath,filename

    def run(self):
        local_send = ps(username=self.username, hostname=self.hostname, remote_dir=self.remote_dir)
        out_dir = "out"
        sent_dir = f"{out_dir}/sent"
        try:
            os.mkdir(out_dir)
        except FileExistsError:
            print(f"directory {out_dir} already exists")
        try:
            os.mkdir(sent_dir)
        except FileExistsError:
            print(f"directory {sent_dir} already exists")
        # warm up and IR baseline
        print("warming up")
        time.sleep(60)
        print("warm up complete")
        while True:
            image = self.cameraCapture(file_path=out_dir)
            time.sleep(1)
            local_send.scpSender(image[0])
            print(f"{image[0]} sent to {self.hostname}")
            shutil.move(image[0], f"{sent_dir}/{image[1]}")
            print(f"{image[0]} moved to ---> {sent_dir}/{image[1]}")
            # terminating the session

trig = pyTrigger(args.username, args.remote_host, args.remote_dir)
trig.run()
