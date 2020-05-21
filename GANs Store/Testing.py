from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk

window = ThemedTk(theme="equilux")
ttk.Button(window, text="Quit", command=window.destroy).pack()
ttk.Button(window, text="Quit", command=window.destroy).pack()
ttk.Entry(window,text="Quit").pack()

 

L1 = ttk.Label(window, text="Label")
L1.pack(side="left")
E1 = ttk.Entry(window)
E1.pack(side="right")

window.mainloop()