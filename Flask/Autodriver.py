import time
import picamera
import numpy as np
import cv2
import gpioController as g
import io

class neuralnet(object):
  def __init__(self):
    self.mode = cv2.ANN_MLP()
  def create(self):
    layer_size = np.int32([38400,32,4])
    self.model.create(layer_size)
    self.model.load('mlp_xml/mlp.xml')
  def predict(self, samples):
    ret, resp = self.model.predict(samples)
    return resp.argmax(-1)

#model = cv2.ANN_MLP()
#layer_size = ([38400,32,4])
#model.create(layer_size)
#model.load('/autrccar/Flask/mlp_xml/mlp.xml')

#def predictor(samples):
  #ret, resp = model.predict(samples)
  #print(ret.argmax(-1))
  #return (ret.argmax(-1))

def steer(prediction):
  if prediction == 2:
    g.forwardGPIO()
  elif prediction == 0:
    g.leftGPIO()
  elif prediction == 1:
    g.rightGPIO()
  else:
    g.stopGPIO()

model = neuralnet()
model.create()
with picamera.PiCamera() as cam:
  cam.resolution = (320,240)
  cam.framerate = 10
  start = time.time()
  stream = io.BytesIO()
  for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
    stream.seek(0)
    jpg = stream.read()
    gray = cv2.imdecode(np.fromstring(jpg,dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
    roi = gray[120:240, :]
    image_array = roi.reshape(1,38400).astype(np.float32)
    print(type(image_array))
    print(image_array.size)
    print(image_array.shape)
    #prediction = predictor(image_array)
    prediction = model.predict(image_array)
    steer(prediction)
    stream.seek(0)
    stream.truncate()
