# <3 from http://courses.csail.mit.edu/6.867/wiki/images/3/3f/Plot-python.pdf

import numpy as np
import matplotlib
matplotlib.use('Agg')  # necessary since we're headless
import matplotlib.pyplot as plt

print("Hello CSI3660 you get to go home early today because I just talked and talked adnt alked and he's still talking.")

## super-basic line plotting
xvals = np.arange(-2, 1, 0.01) # Setup our x-values
yvals = np.cos(xvals)            # Setup our y-values
plt.plot(xvals, yvals)           # Plot a basic X-Y plot
#plt.show()                      # If this were a program with a display, this would show the fig
plt.savefig('plots/sine-plot.png') # Save the figure to PNG (you can use other formats by changing extension)

print "sine-plot.png generated!"
raw_input('[1/3] Press enter to continue to the next step')

## using a quadratic function and annotating a previous figure
newyvals = 1 - 0.5 * xvals**2     # Evaluate quadratic approximation on xvals
plt.plot(xvals, newyvals, 'r--')  # Line plot with red dashed line
plt.title('Example quadratic approximation')

plt.xlabel('Input')
plt.ylabel('Function values')
plt.savefig('plots/quad-plot.png') 

print "quad-plot.png generated!"
raw_input('[2/3] Press enter to continue to the next step')

## generating a contour plot
plt.figure()                         # Create a new figure (otherwise it'd keep drawing on the old one!)
xlist = np.linspace(-2.0, 1.0, 100)  # 1-D arrays for x,y dimensions
ylist = np.linspace(-1.0, 2.0, 100)
X, Y  = np.meshgrid(xlist, ylist)    # Create 2-D grid from xlist and ylist
Z     = np.sqrt(X**2 + Y**2)         # Compute function values on grid

plt.contour(X, Y, Z, [0.5, 1.0, 1.2, 1.5], colors='k', linestyles='solid')
plt.savefig('plots/contour-plot.png')

print "contour-plot.png generated!"
print "[3/3] Done."
