#!/usr/bin/python3

import os
from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta, timezone
import numpy as np
import cv2

jst = timezone(timedelta(hours=+9), 'JST')

w = 2048
h = 1536

camera = PiCamera()
camera.resolution = (w, h)
camera.start_preview()
sleep(5)

prefix = os.environ.get('RASPBERRY_TIMELAPSE_WORK_DIR', '.')

wb = cv2.xphoto.createGrayworldWB()
wb.setSaturationThreshold(0.8)

image = np.empty((w * h * 3,), dtype=np.uint8)

for filename in camera.capture_continuous(image, 'bgr'):
  now = datetime.now(jst)

  time = now.strftime('%H%M%S')
  if '030000' < time < '080000':
    next_hour = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    delay = (next_hour - datetime.now()).seconds
    sleep(delay)
    continue

  timestamp = now.isoformat(timespec='seconds')

  image = image.reshape((h, w, 3))
  result = wb.balanceWhite(image)

  cv2.putText(
    result,
    timestamp,
    (30, 100),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.0,
    (255, 255, 255),
    thickness=2
  )

  dir = (now + timedelta(hours=-3)).strftime('%Y-%m-%d')
  path = '{}/{}'.format(prefix, dir)
  os.makedirs(path, exist_ok=True)

  filename = '{}/{}.jpg'.format(path, timestamp.replace(':', ''))
  cv2.imwrite(filename, result)

  sleep(10)
