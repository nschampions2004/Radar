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
  def __init__(self, figure, filename, row_list, rect=None):
      """ Takes in matplotlib plot area (figure), Pandas data frame,
      and rect (list of left, bottom, width, height) for matplotlib figure
      ## TODO:
        2) Translate list values to Polar Co-ordinates.
            a) Function that takes a list of values (in the example, a list
                of percents) and converts them to polar coordinates.
            b) Plots those points.
      (strings for the end points of the axes) , labels (these are just masks
      over polar plots)
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
      self.AXES_COUNT = len(self.data.index)
      AXES_DEPTH = 7
      # sets the angles in degrees as a numpy array
      self.angles = np.arange(0, 360, 360.0/self.AXES_COUNT)

      # getting maximums- AXES_COUNT maximums
      self.maxes = self.data.max(1)
      # getting minimums- AXES_COUNT minimums
      self.mins = self.data.min(1)

      axes_max = []
      for number in self.maxes:
          while number % AXES_DEPTH != 0:
              number += 1
          axes_max.append(number)


      axes_mins = []
      for number in self.mins:
          while number % AXES_DEPTH != 0:
              number -= 1
          axes_mins.append(number)
      #axes_mins = [0] * len(axes_max)
      # increasing negative axes so range will work
      axes_max = [1 if max == 0 else max for max in axes_max]

      increment_list = [int((axes_max[spot] - axes_mins[spot]) / AXES_DEPTH)
        for spot in range(len(axes_max))]
      min_max_list = [[i, j] for i,j in zip(axes_mins, axes_max)]

      axes_labels = [list(range(min_max_list[j][0], min_max_list[j][1],
        increment_list[j])) for j in range(0, len(min_max_list))]

      for row in row_list:
          axes_labels[row] = axes_labels[row][::-1]
      axes_labels = [label_set[0:7] for label_set in axes_labels]

      self.axes = [figure.add_axes(rect, projection='polar', label='axes%d' % i) for i in range(self.AXES_COUNT)]

      self.ax = self.axes[0]
      self.ax.set_thetagrids(self.angles, labels=self.data.index, fontsize=14)

      for ax in self.axes[1:]:
          ax.patch.set_visible(False)
          ax.grid(False)
          ax.xaxis.set_visible(False)

      for ax, angle, label in zip(self.axes, self.angles, range(len(self.data.index.tolist()))):
          ax.set_rgrids(range(1, AXES_DEPTH + 2), angle=angle, labels=axes_labels[label]) # 6
          ax.spines['polar'].set_visible(False)
          ax.set_ylim(0, AXES_DEPTH + 1)

  def plot(self, values, *args, **kw):
      angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
      values = np.r_[values, values[0]]
      self.ax.plot(angle, values, *args, **kw)

  def plot2(self, *args, **kw):
      plots = self.data.shape[1] - 1
      # need something convert each cols vals to polar co-ordinates

      # get a list of slopes
      # get a list of y-ints




if __name__ == '__main__':
    fig = plt.figure(figsize=(11, 11))


    radar = Radar(fig, 'data.csv', [1, 2, 3, 4, 5, 9, 10])
    radar.plot([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
               ,  '-', lw=3, color='b', alpha=0.4, label='1')
    radar.plot([4.60, 4.10, 5.45, 5.60, 4.83, 4.57, 4.78, 5.00, 4.78, 5.00, 4.83]
               , '-', lw=3, color='r', alpha=0.4, label='2')
    radar.plot([4.60, 3.80, 5.45, 5.60, 3.83, 4.29, 5.01, 5.00, 4.94, 4.75, 4.33]
               , '-', lw=3, color='g', alpha=0.4, label='3')
    radar.plot([4.60, 4.50, 5.45, 5.65, 5.83, 4.79, 4.55, 5.00, 4.62, 5.50, 5.17]
               , '-', lw=3, color='y', alpha=0.4, label='4')
    radar.plot2()
    radar.ax.legend()
    plt.savefig('attempt.png', bbox_inches = 'tight', dpi = 500)
