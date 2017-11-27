# https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

import numpy as np
import matplotlib as mpl
mpl.use('Agg')  # necessary since we're headless
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

mpl.rcParams['legend.fontsize'] = 10

fig   = plt.figure()
ax    = fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z     = np.linspace(-2, 2, 100)
r     = z**2 + 1
x     = r * np.sin(theta)
y     = r * np.cos(theta)
ax.plot(x, y, z, label='parametric curve')
ax.legend()

plt.savefig('plots/3d-line-plot.png')
print "3d-line-plot.png generated!"
raw_input('[1/3] Press enter to continue to the next step')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.05)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.savefig('plots/3d-wireframe-plot.png')
print "3d-wireframe-plot.png generated!"
raw_input('[2/3] Press enter to continue to the next step')

n_radii = 8
n_angles = 36

# Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
radii = np.linspace(0.125, 1.0, n_radii)
angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)

# Repeat all angles for each radius.
angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)

# Convert polar (radii, angles) coords to cartesian (x, y) coords.
# (0, 0) is manually added at this stage,  so there will be no duplicate
# points in the (x, y) plane.
x = np.append(0, (radii*np.cos(angles)).flatten())
y = np.append(0, (radii*np.sin(angles)).flatten())

# Compute z to make the pringle surface.
z = np.sin(-x*y)

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)

plt.savefig('plots/3d-triangular-plot.png')
print "3d-triangular-plot.png generated!"
print '[3/3] Done.'
