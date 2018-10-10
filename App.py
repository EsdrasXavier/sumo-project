from Video import *
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:

	def __init__(self, window, window_title, video_source=0):
		'''Initializer da classe
		'''
		self.timer = 1
		self._start = 0.0
		self._elapsedtime = 0.0

		self.window = window
		self.window.title(window_title)

		self.vid = Video(video_source)

		self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
		self.canvas.pack()

		self.counter = tkinter.Label(self.window, text="Timer: 00:00:00")
		self.counter.pack(side=tkinter.LEFT)

		take_snapshot = tkinter.Button(self.window, text="Iniciar", command=self.start_monitoring)
		take_snapshot.pack(side=tkinter.LEFT)

		reset = tkinter.Button(self.window, text="Reset", command=self.reset_monitoring)
		reset.pack(side=tkinter.LEFT)


		self.update()
		self.window.mainloop()

	def _update(self):
		'''Atualiza o valor do timer
		'''
		self._elapsedtime = time.time() - self._start
		self._setTime(self._elapsedtime)

		minutes = int(self._elapsedtime / 60)
		seconds = int(self._elapsedtime - minutes * 60.0)

		if seconds >= 5:
			self.vid.take_snapshot("tomada_" + str(self.timer))
			return

		self._timer = self.window.after(1, self._update)

	def _setTime(self, elap):
		'''Exibe o valor do timer na label para um retorno visual do usuário
		'''
		minutes = int(elap / 60)
		seconds = int(elap - minutes * 60.0)
		hseconds = int((elap - minutes * 60.0 - seconds) * 100)
		self.counter.config(text='Timer: %02d:%02d:%02d' % (minutes, seconds, hseconds))


	def start_monitoring(self):
		'''Inicia o monitoramento
		'''
		self.vid.take_snapshot("tomada_" + str(self.timer))
		self._start = time.time() - self._elapsedtime
		self._update()


	def reset_monitoring(self):
		'''Reseta todos os valores e incrementa para proxima tomada
		'''
		self._start = 0.0
		self._elapsedtime = 0.0
		self.timer += 1
		self.counter.config(text='Timer: 00:00:00')


	def update(self):
		'''Fica atualizando a tela e mostrando a imagem que é pega
		de dentro da classe de video.
		'''
		ret, frame = self.vid.get_frame()

		if ret:
			self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
			self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
		self.window.after(15, self.update)

