import zmq
from struct import pack, unpack
import time
import cv2
import os

UPLOAD_FOLDER = "./static/uploads/"

context = zmq.Context()  
socket = context.socket(zmq.PAIR)
socket.connect("tcp://127.0.0.1:8000")

#Commands to send images
CMD_SEND_IMAGE = 0x01
CMD_NUM_IMAGE = 0x02
CMD_USER_EMAIL = 0x03

def pack_response(cmd, p0, p1, p2, p3):
    packed_str =(pack('!I',cmd)+pack('!I',p0)+pack('!I',p1)+pack('!I',p2)+pack('!I',p3))
    return packed_str

def maintain_aspect_ratio(img):
    height, width = img.shape[:2]
    if height > width:
        diff = int((height-width)/2)
        crop_img = cv2.copyMakeBorder(img, top=0, bottom=0, left=diff, right=diff, 
        borderType = cv2.BORDER_CONSTANT, value=(0, 0, 0))
    elif width > height:
        diff =int((width-height)/2)
        crop_img = cv2.copyMakeBorder(img,top = diff, bottom = diff, left=0, right=0,borderType= cv2.BORDER_CONSTANT,value=(0, 0, 0))
    return crop_img
    
def send_images_to_server(email_id):
    images = os.listdir(UPLOAD_FOLDER)
    message = ""
    message += pack_response(CMD_NUM_IMAGE, len(images), 0, 0, 0)
    for i in images:
        img = cv2.imread(os.path.join(UPLOAD_FOLDER,i))
        img = maintain_aspect_ratio(img)
        img = cv2.resize(img, (227, 227))
        img = img.flatten()
        message += img.tobytes()
        os.remove(os.path.join(UPLOAD_FOLDER,i))
    message += email_id
