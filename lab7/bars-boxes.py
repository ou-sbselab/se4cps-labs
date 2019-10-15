# https://matplotlib.org/examples/pylab_examples/boxplot-demo.html
# https://pythonspot.com/en/matplotlib-bar-chart/

import matplotlib
matplotlib.use('Agg')  # necessary since we're headless
import matplotlib.pyplot as plt
import numpy as np

## NOTE: this code is translated directly from those websites above.

## bar charts

objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(objects))
performance = [10,8,6,4,2,1]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Programming language usage')
 
plt.savefig('plots/barcharts-plot.png')
print("barcharts-plot.png generated!")
input('[1/4] Press enter to continue to the next step')

## boxplots

# fake up some data
spread = np.random.rand(50) * 100
center = np.ones(25) * 50
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100
data = np.concatenate((spread, center, flier_high, flier_low), 0)

# basic plot
plt.boxplot(data)
plt.savefig('plots/boxplot-1-plot.png')
print("boxplot-1-plot.png generated!")
input('[2/4] Press enter to continue to the next step')

# horizontal boxes
plt.figure()
plt.boxplot(data, 0, 'rs', 0)
plt.savefig('plots/boxplot-2-plot.png')
print("boxplot-2-plot.png generated!")
input('[3/4] Press enter to continue to the next step')

# fake up some more data
spread = np.random.rand(50) * 100
center = np.ones(25) * 40
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100
d2 = np.concatenate((spread, center, flier_high, flier_low), 0)
data.shape = (-1, 1)
d2.shape = (-1, 1)
# data = concatenate( (data, d2), 1 )
# Making a 2-D array only works if all the columns are the
# same length.  If they are not, then use a list instead.
# This is actually more efficient because boxplot converts
# a 2-D array into a list of vectors internally anyway.
data = [data, d2, d2[::2, 0]]
# multiple box plots on one figure
plt.figure()
plt.boxplot(data)

plt.savefig('plots/boxplot-3-plot.png')
print("boxplot-3-plot.png generated!")
print('[4/4] Done.')
