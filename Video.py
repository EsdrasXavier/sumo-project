import argparse
from collections import deque
import cv2
from imutils.video import VideoStream
import imutils
import numpy as np
from tkinter import *
import time
import os, errno


class Video:

	def __init__(self, video_source=0):
		'''Initializer da classe
		'''

		self.lower = {}
		self.upper = {}

		self.photo_counter = 0
		self.vid = cv2.VideoCapture(video_source)

		ap = argparse.ArgumentParser()
		ap.add_argument("-v", "--video",
			help="path to the (optional) video file")
		ap.add_argument("-b", "--buffer", type=int, default=64,
			help="max buffer size")

		self.args = args = vars(ap.parse_args())
		self.pts = deque(maxlen=args["buffer"])


		if not self.vid.isOpened():
			raise ValueError("Unable to open camera ", video_source)

		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)


	def __del__(self):
		'''Deleta a classe
		'''
		if self.vid.isOpened():
			self.vid.release()


	def add_to_upper(self, color_name, hsv):
		'''Adiciona uma nova cor ao filtro de cor mais alto
		'''
		self.upper[color_name] = hsv


	def add_to_lower(self, color_name, hsv):
		'''Adiciona uma nova cor ao filtro de cor mais baixo
		'''
		self.lower[color_name] = hsv


	def get_frame(self):
		'''Pega o video junto com o identificador de cores
		'''
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			frame = self.make_circle_on_obj(frame)

			if ret:
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)


	def make_circle_on_obj(self, frame):
		'''Faz um circulo no frame que possui uma das cores abaixo,
		e retorna o frame
		'''
		upper, lower = self.upper, self.lower

		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		for key, value in upper.items():
			mask = cv2.inRange(hsv, lower[key], upper[key])
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[0] if imutils.is_cv2() else cnts[1]

			center = None

			if len(cnts) > 0:
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				if radius > 10:
					cv2.circle(frame, (int(x), int(y)), int(radius),
						(0, 255, 255), 2)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)

					self.pts.appendleft(center)

					# Caso queira uma linha seguindo o ponto descomente o código abaixo
					# for i in range(1, len(self.pts)):
					# 	if self.pts[i - 1] is None or self.pts[i] is None:
					# 		continue

					# 	thickness = int(np.sqrt(self.args["buffer"] / float(i + 1)) * 2.5)
					# 	if str(key) == 'red':
					# 		cv2.line(frame, self.pts[i - 1], self.pts[i], (128, 0, 255), thickness)
					# 	else:
					# 		cv2.line(frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)

		return frame


	def take_snapshot(self, path="test"):
		'''Tira print da tela atual (somente do video) e salva
		'''

		try:
			os.makedirs(str(path))
		except OSError as e:
			print(e)

		ret, frame = self	.get_frame()
		if ret:
			self.photo_counter += 1

			if self.photo_counter > 2:
				self.photo_counter = 1

			cv2.imwrite(path + "/frame-" + str(self.photo_counter) + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

