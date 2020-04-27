import cv2
import numpy as np
import queue
import threading
import time

class BufferlessVideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)
    
  def setAttributes(self, arg1, arg2):
      self.cap.set(arg1, arg2)

  def read(self):
    return self.q.get()

class Reader:
    def __init__(self, input, isVideo):
        self.video = isVideo
        if isVideo:
            self.capture = cv2.VideoCapture(input)
            print("Input mode: video")
        else:
            self.capture = BufferlessVideoCapture(input)
            print("Input mode: camera stream")

    def get_frame(self):
        if self.video:
            ret, img = self.capture.read()
            if not ret:
                raise ValueError("Video is out of frames")
            else:
                return img
        else:
            return self.capture.read()

        