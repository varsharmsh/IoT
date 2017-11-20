import zmq
from struct import pack, unpack
import time
import cv2
import os

UPLOAD_FOLDER = "./static/uploads/"

context = zmq.Context()  
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:8000")

#Commands to send images
CMD_SEND_IMAGE = 0x01
CMD_NUM_IMAGE = 0x02
CMD_IS_ALIVE = 0x03
CMD_READY_TRAIN = 0x04
CMD_SEND_NAME = 0x05
CMD_NAME = 0x06

def pack_response(cmd, p0, p1, p2, p3):
    packed_str =(pack('!I',cmd)+pack('!I',p0)+pack('!I',p1)+pack('!I',p2)+pack('!I',p3))
    return packed_str

def parse_header(hdr):
    """
    unpack data header sent by client 
    """
    x = unpack('!IIIII', hdr);
    return x[0], x[1], x[2], x[3], x[4]

def maintain_aspect_ratio(img):
    height, width = img.shape[:2]
    if height > width:
        diff = int((height-width)/2)
        crop_img=cv2.copyMakeBorder(img, top=0, bottom=0, left=diff, right=diff, 
        borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0))
    elif width > height:
        diff =int((width-height)/2)
        crop_img =cv2.copyMakeBorder(img,top = diff, bottom = diff, left=0, right=0,borderType= cv2.BORDER_CONSTANT,value=(0, 0, 0))
    return crop_img
    
def send_images_to_server(email_id,name):    
    info = pack_response(CMD_IS_ALIVE,0,0,0,0)+ str.encode(email_id)
    socket.send(info)
    message = socket.recv()
    cmd, par0, par1, par2, data_length  = parse_header(message[0:20])
    if cmd == CMD_READY_TRAIN:
        images = os.listdir(UPLOAD_FOLDER)
        message = pack_response(CMD_SEND_IMAGE, len(images), 0, 0, 0)
        for i in images:
            img = cv2.imread(os.path.join(UPLOAD_FOLDER,i))
            img = cv2.imread(i)
            img = maintain_aspect_ratio(img)
            img = cv2.resize(img, (227, 227))
            img = img.flatten()
            message += img.tobytes()
            os.remove(os.path.join(UPLOAD_FOLDER,i))
        socket.send(message)
        message = socket.recv()
        cmd, par0, par1, par2, data_length  = parse_header(message[0:20])
        if cmd != CMD_SEND_NAME:
            return
        info = pack_response(CMD_NAME,0,0,0,0) + str.encode(name)
        socket.send(info)
        #message += email_id


