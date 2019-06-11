#Tkinter libraries
import tkinter as tk
from tkinter import messagebox as msgb
from tkintertable import TableCanvas, TableModel

#Matplotlib libraries
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
import matplotlib.animation as animation

#Other libraries
import random

programTitle = "Galvanic Skin Response UI"
programIcon = "icon.gif"
pacientName = None

#Inicial vector with random numbers for testing
vectorx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
vectory = [3, 5, 8, 9, 9, 7, 6, 3, 2, 1, 7]

f = Figure(figsize=(5.5, 4))
f.suptitle('Name of the graph', fontsize=14, fontweight='bold')
a = f.add_subplot(111)

def startWindow():
	StartWindow = tk.Tk()
	StartWindow.title(programTitle)

	StartWindow.tk.call('wm', 'iconphoto', StartWindow._w, tk.PhotoImage(file=programIcon))

	AuxLabel1 = tk.Label(StartWindow,
						text=None)

	StartLabel = tk.Label(StartWindow,
							text="Main menu",
							font="Calibri 14")

	MainPacientLabel = tk.Label(StartWindow,
								text="The pacient is " + pacientName,
								font="Calibri 10")

	TableFrameStart = tk.Frame(StartWindow)

	#tabela = tk.Label(StartWindow,
	#					text="A tabela fica aqui!",
	#					bg="gray")

	#grafico = tk.Label(StartWindow,
	#					text="O grafico fica aqui!",
	#					bg="gray")
	
	AuxLabel1.pack(side=tk.TOP, pady=5)
	StartLabel.pack(side=tk.TOP, padx=100, pady=10)
	MainPacientLabel.pack(side=tk.TOP)

	#tabela.pack(side=tk.LEFT, padx=25, pady=25, ipadx=200, ipady=200)
	TableFrameStart.pack(side=tk.LEFT)
	#grafico.pack(side=tk.RIGHT, padx=25, pady=25, ipadx=200, ipady=200)

	data = {
		'r1':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r2':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r3':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r4':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r5':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r6':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r7':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r8':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r9':  {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r10': {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r11': {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0},
    	'r12': {'Time': 0, 'Voltage': 0, 'Current': 0, 'Impedance': 0}
    }

	TableModelStart = TableModel()

	TableStart = TableCanvas(TableFrameStart,
							model=TableModelStart,
							cellwidth=120,
							columnheight=40,
							editable=False
							)
	TableModelStart.importDict(data)
	TableStart.setSelectedRow(-1)
	TableStart.show()

	#Changing values
	TableModelStart.setValueAt(5, 0, 0)
	TableStart.redrawTable()

	#Ploting a graph in the interface
	a.plot(vectorx,vectory)
	a.set_xlabel('X axis')
	a.set_ylabel('Y axis')
	canvas = FigureCanvasTkAgg(f, master= StartWindow)
	canvas.draw()
	canvas.get_tk_widget().pack(side = tk.RIGHT, expand = False, ipadx=2, ipady=2, padx=25, pady=25)

	#Calls the function to pdate the graph
	ani = animation.FuncAnimation(f, animate, interval=100, blit=False)	
	StartWindow.mainloop()

#Function that updates the information in the graph
def animate(f):
	vectory.pop(0)
	vectory.append(random.randint(1,10))
	for i in range(0, len(vectorx)):
		vectorx[i] =  vectorx[i]+1
        
	a.clear()
	a.set_xlabel('X axis')
	a.set_ylabel('Y axis')
	a.plot(vectorx,vectory, 'ro', vectorx,vectory, 'k')

def loginWindow():
	
	def buttonLoginEnter():
		global pacientName
		pacientName = LoginEntryWidget.get()
		if pacientName == "Insert here the pacient's name" or pacientName == "":
			msgb.showerror("Error", "Put a valid name.")
		else:
			LoginWindow.destroy()
			startWindow()

	LoginWindow = tk.Tk()
	LoginWindow.title(programTitle)
	LoginWindow.tk.call('wm', 'iconphoto', LoginWindow._w, tk.PhotoImage(file=programIcon))

	LoginLabel = tk.Label(LoginWindow,
							text="Insert the pacient name below.",
							font="Calibri 14")

	LoginEntryWidget = tk.Entry(LoginWindow)
	LoginEntryWidget.insert(10, "Insert here the pacient's name")

	LoginButtonConfirm = tk.Button(LoginWindow,
									text="Confirm",
									command=buttonLoginEnter)


	LoginLabel.pack(side=tk.TOP, padx=100, pady=40)
	LoginButtonConfirm.pack(side=tk.BOTTOM, padx=150, pady=40, fill=tk.X)
	LoginEntryWidget.pack(side=tk.BOTTOM, padx=100, pady=20, fill=tk.X)

	LoginWindow.mainloop()

loginWindow()