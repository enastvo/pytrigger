# motion detector stuff
from gpiozero import MotionSensor
import time
import datetime
import picamera

# email stuff
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import argparse

parser = argparse.ArgumentParser(description="start up the PIR sensor")
parser.add_argument("fromAddr", help="enter the from email address", type=str)
parser.add_argument("toAddr", help="enter the to email address", type=str)
parser.add_argument("pwd", help="enter the password for the from email account", type=str)
args = parser.parse_args()

class pyTrigger:

    def __init__(self, fromAddr, toAddr, pwd, m=4):
        self.fromAddr = fromAddr
        self.toAddr = toAddr
        self.pwd = pwd
        self.motionsense = m
        self.pir = MotionSensor(self.motionsense)
        self.camera = picamera.PiCamera()


    def getFileName(self):
        return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")

    def compileMessage(self, filename):
        toAddr = self.toAddr
        fromAddr = self.fromAddr
        pwd = self.pwd
        msg = MIMEMultipart()
        # storing the senders email address
        msg['From'] = fromAddr
        # storing the receivers email address
        msg['To'] = toAddr
        # storing the subject
        msg['Subject'] = f"Motion Detector Alert, image captured: {filename}"
        # string to store the body of the mail
        body = "This is an auto-generated message prompted by a motion detection"
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        # open the file to be sent
        # filename = "File_name_with_extension"
        attachment = open(filename, "rb")
        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        # To change the payload into encoded form
        p.set_payload((attachment).read())
        # encode into base64
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename= {filename}")
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication## You must enter your password here, or recode.  I understand the risks of a hardcoded password :(
        s.login(fromAddr, pwd)
        # Converts the Multipart msg into a string
        text = msg.as_string()
        # sending the mail
        s.sendmail(fromAddr, toAddr, text)
        s.quit()
        print(f"motion captured {filename} image emailed to {toAddr}. More reports to follow.")
        time.sleep(10)

    def cameraCapture(self):
        # waiting for motion
        self.pir.wait_for_motion()
        if self.pir.motion_detected:
            # text to print for good feelings
            print("intruder detected")
            # set file name now that detection has happened
            filename = self.getFileName()
            # these steps for picamera
            self.camera.resolution = (2592, 1944)
            # for debugging
            # camera.start_preview()
            time.sleep(0.1)
            self.camera.capture(filename)
            print("intruder image saved " + filename)
            return filename

    def run(self):
        # warm up and IR baseline
        print("warming up")
        time.sleep(60)
        print("warm up complete")
        while True:
            image = self.cameraCapture()
            self.compileMessage(image)
            # terminating the session

trig = pyTrigger(args.fromAddr, args.toAddr, args.pwd)
trig.run()

