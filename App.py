import cv2
import os, sys
import PIL.Image, PIL.ImageTk
import time
import re

from Video import *


try:    # Python 2
	import Tkinter as tk
	from Tkinter import messagebox
	import tkFont
except:  # Python 3
	import tkinter as tk
	from tkinter import messagebox
	import tkinter.font as tkFont



class App:

	def __init__(self, window, window_title, video_source=0):
		'''Initializer da classe
		'''
		self.window = window
		self.window.title(window_title)

		BUTTON_FONT_STYLE = tkFont.Font(self.window, family="Helvetica", size=10)
		BUTTON_PADX = (3, 3)
		BUTTON_PADY = (5, 20)

		self.timer = 1
		self.already_started = False
		self._elapsedtime = self._start = 0.0
		self.folder_to_compare = ["--"]


		self.vid = Video(video_source)

		self.vid.add_to_lower('red', (166, 84, 141))
		self.vid.add_to_upper('red', (186,255,255))

		self.vid.add_to_lower('green', (25, 189, 118))
		self.vid.add_to_upper('green', (95, 255, 255))

		self.take_number = tk.Label(self.window, text="Tomada número 1", font=tkFont.Font(family="Helvetica", size=15))
		self.take_number.pack(anchor=tk.CENTER)
		self.counter = tk.Label(self.window, text="Timer: 00:00:00", font=BUTTON_FONT_STYLE)
		self.counter.pack(anchor=tk.CENTER, padx=BUTTON_PADX, pady=BUTTON_PADY)

		self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
		self.canvas.pack(anchor=tk.CENTER)


		take_snapshot = tk.Button(self.window, text="Iniciar", command=self.start_monitoring,
															font=BUTTON_FONT_STYLE)
		take_snapshot.pack(side=tk.LEFT, padx=BUTTON_PADX, pady=BUTTON_PADY)

		reset = tk.Button(self.window, text="Reset", command=self.reset_monitoring,
											font=BUTTON_FONT_STYLE)
		reset.pack(side=tk.LEFT, padx=BUTTON_PADX, pady=BUTTON_PADY)

		show_takes = tk.Button(self.window, text="Comparar", command=self.show_takes,
													 font=BUTTON_FONT_STYLE)
		show_takes.pack(side=tk.LEFT, padx=BUTTON_PADX, pady=BUTTON_PADY)

		self.path_to_compare = tk.StringVar(self.window)

		self.drop_menu = tk.OptionMenu(self.window, self.path_to_compare, *self.folder_to_compare)
		self.drop_menu.config(width=15)
		self.drop_menu.pack(side=tk.LEFT, padx=BUTTON_PADX, pady=BUTTON_PADY)

		self.update_list()
		self.update()
		self.window.mainloop()


	def show_takes(self):
		'''Exibe as tomas já feitas
		'''

		try:
			path = self.path_to_compare.get()
			if 'tomada' in path:
				self.vid.compare_images(path)
			else:
				messagebox.showerror("Erro", "Tomada de tempo inexistente")

		except:
			messagebox.showerror("Erro", "Erro ao realizar comparação de imagens. Arquivos não encontrados ou arquivos corrompidos.")
			print(self.path_to_compare.get())
			print("Um erro desconhecido aconteceu. Erro: {}".format(sys.exc_info()))


	def get_list_to_compare(self):
		'''Busca todos os arquivos de tomadas na pasta atual
		'''
		folder_to_show = list()

		try:
			my_folders = [x[0] for x in os.walk(".\\")]
			for i in my_folders:
				for j in i.split('\\'):
					if 'tomada' in j:
						folder_to_show.append(j)
		except:
			messagebox.showerror("Error", "Erro ao buscar arquivos para comparar")

		folder_to_show.sort(key=self.natural_keys)

		return folder_to_show


	def update_list(self):
		'''Atualiza o drop down de menu com todas as pastas
		disponiveis para comparar
		'''
		self.folder_to_compare = self.get_list_to_compare()

		menu = self.drop_menu['menu']
		menu.delete(0, 'end')

		for path in self.folder_to_compare:
			menu.add_command(label=path, command=lambda value=path: self.path_to_compare.set(value))


	def _update(self):
		'''Atualiza o valor do timer
		'''
		self._elapsedtime = time.time() - self._start
		self._setTime(self._elapsedtime)

		minutes = int(self._elapsedtime / 60)
		seconds = int(self._elapsedtime - minutes * 60.0)

		if seconds >= 5:
			self.vid.take_snapshot("tomada_" + str(self.timer))
			self.update_list()
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
		if self.already_started:
			return

		self.already_started = True
		self.vid.take_snapshot("tomada_" + str(self.timer))
		self._start = time.time() - self._elapsedtime
		self._update()


	def reset_monitoring(self):
		'''Reseta todos os valores e incrementa para proxima tomada
		'''
		self.timer += 1
		self.already_started = False
		self._elapsedtime = self._start = 0.0
		self.counter.config(text='Timer: 00:00:00')
		self.take_number.config(text="Tomada número " + str(self.timer))


	def update(self):
		'''Fica atualizando a tela e mostrando a imagem que é pega
		de dentro da classe de video.
		'''
		ret, frame = self.vid.get_frame()

		if ret:
			self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
			self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
		self.window.after(15, self.update)


	def atoi(self, text):
		return int(text) if text.isdigit() else text


	def natural_keys(self, text):
		'''
		alist.sort(key=natural_keys) Organiza na forma 'humana'
		http://nedbatchelder.com/blog/200712/human_sorting.html
		'''
		return [ self.atoi(c) for c in re.split('(\d+)', text) ]