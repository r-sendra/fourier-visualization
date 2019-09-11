import math,turtle
import numpy as np
import time
import tkinter
import pdb
import matplotlib.pyplot as plot

DELTA_THETA = 0.01
RADIUS = 100
CENTER = (250, 450)
DRAW_WIDTH = 2

armonics = list(range(1,9,2))

#fn = lambda n: (CENTER[0] + RADIUS + RADIUS/armonics[n-1] + 2*np.sum([RADIUS/armonics[i-1] for i in np.arange(2,n)]), CENTER[1])
fn = lambda n: (CENTER[0] + np.sum([RADIUS/armonics[i] for i in np.arange(0,n)]), CENTER[1])

centers = np.array(list(map(fn, np.arange(len(armonics)))))

root = tkinter.Tk()
root.geometry('1000x900')

c = tkinter.Canvas(root, height=900, width=1000, bg='black')
c.pack()


circle_ids = []
arrow_ids = []

# first circle (fundamental freq)
circle_ids.append(c.create_oval(centers[0][0]-RADIUS, centers[0][1]-RADIUS, centers[0][0]+RADIUS, centers[0][1]+RADIUS, outline='white', width=DRAW_WIDTH))
arrow_ids.append(c.create_line(centers[0][0], centers[0][1],centers[0][0]+RADIUS, centers[0][1], fill='red', width=3))
for i, arm in enumerate(armonics[1:]):
    i += 1
    circle_ids.append(c.create_oval(centers[i][0]-RADIUS/arm, centers[i][1]-RADIUS/arm, 
                    centers[i][0]+RADIUS/arm, centers[i][1]+RADIUS/arm, outline='white', width=DRAW_WIDTH))
    arrow_ids.append(c.create_line(centers[i][0], centers[i][1], 
                        centers[i][0]+RADIUS/arm, centers[i][1], fill='red', width=DRAW_WIDTH))
                

prev_xy = (centers[-1][0] + RADIUS/armonics[-1], centers[-1][1])
plotter = c.create_line(prev_xy[0], prev_xy[1], 600, 2*(prev_xy[1]-centers[0][1])+400, fill='white', width=DRAW_WIDTH)
plot_vals = (450)*np.ones(3000)
plot_lines = np.array([c.create_line(600, 600, 600+0.1*i, 600, fill='white', width=DRAW_WIDTH) for i in range(2999)])
for theta in np.arange(0, 60, DELTA_THETA):
    for i, f in enumerate(armonics):

        if i > 0:
            centers[i][0] = centers[i-1][0] + (RADIUS/armonics[i-1])*np.cos(armonics[i-1]*theta)
            centers[i][1] = centers[i-1][1] + (RADIUS/armonics[i-1])*np.sin(-armonics[i-1]*theta)
        c.coords(circle_ids[i], centers[i][0]-RADIUS/armonics[i], centers[i][1]-RADIUS/armonics[i],  centers[i][0]+RADIUS/armonics[i], centers[i][1]+RADIUS/armonics[i] )
        arrow_xy = c.coords(arrow_ids[i])
        c.coords(arrow_ids[i], centers[i][0], centers[i][1], 
                centers[i][0] + (RADIUS/f)*np.cos(f*theta), centers[i][1] + (RADIUS/f)*np.sin(-f*theta)) # change coordinates

        if theta < 2*np.pi:
            c.create_line(prev_xy[0], prev_xy[1], centers[-1][0]+(RADIUS/armonics[-1])*np.cos(armonics[-1]*theta),
                                  centers[-1][1]+(RADIUS/armonics[-1])*np.sin(-armonics[-1]*theta), fill='yellow', width=DRAW_WIDTH)
        
        prev_xy = (centers[-1][0]+(RADIUS/armonics[-1])*np.cos(armonics[-1]*theta), centers[-1][1] + (RADIUS/armonics[-1])*np.sin(-armonics[-1]*theta))
        
        c.coords(plotter, prev_xy[0], prev_xy[1], 600, 200 + 1.5*prev_xy[1]-centers[0][1])

        if plot_vals.shape[0] < 3000:
            plot_vals[i] = 200 + 1.5*prev_xy[1]-centers[0][1]
        else:
            plot_vals= np.hstack((200 + 1.5*prev_xy[1]-centers[0][1], plot_vals))

        for i, line in enumerate(plot_lines):
            c.coords(line, 600+0.1*i, plot_vals[i], 600+0.1*(i+1), plot_vals[i+1])

    # print(theta)
       

    c.update()
    root.after(1)















