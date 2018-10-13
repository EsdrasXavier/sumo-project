from App import *
from tkinter import *


try:    # Python 2
  from Tkinter import *
except:  # Python 3
	from tkinter import *


if __name__ == "__main__":
  App(Tk(), "Projeto fabrica")