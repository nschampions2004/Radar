import numpy as np
import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
import pdb


# Optionally use different styles for the graph
# Gallery: http://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
# import matplotlib
# matplotlib.style.use('dark_background')  # interesting: 'bmh' / 'ggplot' / 'dark_background'


class Radar(object):
  def __init__(self, figure, filename, row_list=None, rect=None):
      """ Takes in matplotlib plot area (figure), Pandas data frame,
      and rect (list of left, bottom, width, height) for matplotlib figure
      (strings for the end points of the axes) , labels (these are just masks
      over polar plots).

      The index or left most column is the number of axes.  Additionally, each
      column is a
      """
      if rect is None:
          rect = [0.05, 0.05, 0.9, 0.9]

      try:
          self.data = pd.read_csv('data/' + filename,
                        index_col = 0)
      except FileNotFoundError:
          print('This file does not exist or the path is not correct.')
      else:
          print('The data frame has {} rows and {} columns.' \
            .format(*self.data.shape))

      # set the qualifying axes characteristics
      self.AXES_COUNT = len(self.data.index)
      self.AXES_DEPTH = 7

      # sets the angles in degrees as a numpy array
      self.angles = np.arange(0, 360, 360.0/self.AXES_COUNT)

      # getting maximums- AXES_COUNT maximums
      self.maxes = self.data.max(1)
      # getting minimums- AXES_COUNT minimums
      self.mins = self.data.min(1)

      # walk out till your axes are are divisible by AXES_DEPTH
      axes_max = []
      for number in self.maxes:
          while number % self.AXES_DEPTH != 0:
              number += 1
          axes_max.append(number)
      axes_mins = []
      for number in self.mins:
          while number % self.AXES_DEPTH != 0:
              number -= 1
          axes_mins.append(number)


      # increasing negative axes so range will work
      axes_max = [1 if max == 0 else max for max in axes_max]

      # find how each axes should be incremented by
      self.increment_list = [int((axes_max[spot] - axes_mins[spot]) / self.AXES_DEPTH)
        for spot in range(len(axes_max))]
      min_max_list = [[int(min), int(max)] for min,max in zip(axes_mins, axes_max)]

      axes_labels = [list(range(min_max_list[min_max_pair][0],
        min_max_list[min_max_pair][1], self.increment_list[min_max_pair]))
            for min_max_pair in range(0, len(min_max_list))]

      # flip negative-based axes to go in opposite order
      if row_list:
          for row in row_list:
              axes_labels[row] = axes_labels[row][::-1]
          axes_labels = [label_set[0:AXES_DEPTH] for label_set in axes_labels]

      self.axes = [figure.add_axes(rect, projection='polar', label='axes%d' % i)
        for i in range(self.AXES_COUNT)]

      self.ax = self.axes[0]
      self.ax.set_thetagrids(self.angles, labels=self.data.index, fontsize=14)

      for ax in self.axes[1:]:
          ax.patch.set_visible(False)
          ax.grid(False)
          ax.xaxis.set_visible(False)

      for ax, angle, label in zip(self.axes, self.angles, range(len(self.data.index.tolist()))):
          ax.set_rgrids(range(1, self.AXES_DEPTH + 2), angle=angle, labels=axes_labels[label]) # 6
          ax.spines['polar'].set_visible(False)
          ax.set_ylim(0, self.AXES_DEPTH + 1)


  def plot(self, *args, **kw):
      plots = self.data.shape[1] - 1

      # calculate slopes and intercepts
      slopes = [(self.AXES_DEPTH - 1) / (self.maxes[i] - self.mins[i])
        for i in range(len(self.maxes))]
      int = [(self.AXES_DEPTH - 1) - (slopes[i] * self.maxes.tolist()[i])
        for i in range(len(self.maxes))]

      # normalize values between 1 and AXES_DEPTH
      plots_frame = self.data.apply(lambda x: x * slopes + int + 1, axis = 0)
      angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
      values = plots_frame.to_numpy().tolist()

      # plot the lines
      for row in values:
          row = np.r_[row, row[0]]
          self.ax.plot(angle, row)




if __name__ == '__main__':
    fig = plt.figure(figsize=(11, 11))


    radar = Radar(fig, 'data_small.csv')
    radar.plot()
    radar.ax.legend()
    plt.savefig('attempt.png', bbox_inches = 'tight', dpi = 500)
