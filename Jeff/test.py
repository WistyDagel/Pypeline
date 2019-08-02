from tkinter import *

root = Tk()
root.title('Demo Pypeline')

window_width = 800
window_height = 600

grid_bg = '#0d0e22'
grid_lines = '#508ac9'

loop_time = 10

canvas = Canvas(
    root,
    width=window_width,
    height=window_height,
    bg=grid_bg
)
canvas.grid(column=0, row=0)


def main_loop():

    

    canvas.after(loop_time, main_loop)


root.mainloop()
main_loop()
