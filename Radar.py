import numpy as np
import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt

# Optionally use different styles for the graph
# Gallery: http://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
# import matplotlib
# matplotlib.style.use('dark_background')  # interesting: 'bmh' / 'ggplot' / 'dark_background'


class Radar(object):
  def __init__(self, figure, filename, rect=None):
      """ Takes in matplotlib plot area (figure), titles for the axes
      (strings for the end points of the axes) , labels (these are just masks
      over polar plots), and rect (list of left, bottom, width, height) for
      matplotlib figure
      ## TODO:
        1) Programmatically generate axes min, max and every value in between.
        2) Translate list values to Polar Co-ordinates.
            a) Function that takes a list of values (in the example, a list of percents)
                and converts them to polar coordinates.
            b) Plots those points.
        3)
      """
      if rect is None:
          rect = [0.05, 0.05, 0.9, 0.9]
      # pull in the data
      self.data = pd.read_csv('data/' + filename)

      # how many axes for the graph
      self.n = len(self.data.index)
      # how deep should the axes go
      AXES_DEPTH = 6
      # sets the angles in degrees as a numpy array
      self.angles = np.arange(0, 360, 360.0/self.n)

      # getting maximums- 11 maximums
      self.maxes = self.data.max(1)
      # getting minimums- 11 minimums
      self.mins = self.data.min(1)

      # getting a list of values between these
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
      print(len(axes_mins), len(axes_max))
      # get the increment for each axes
      increment_list = [(axes_max[spot] - axes_mins[spot]) / AXES_DEPTH for spot in range(0,len(axes_max))]
      import pdb
      axes_marker = []
      for spot in range(0, len(axes_max)):
          temp_list = []
          for tick_mark in range(axes_min[spot], axes_max[spot]):
              pdb.set_trace()
              tick_mark += increment_list[spot]
              temp_list = temp_list.append(tick_mark)
          axes_marker = axes_marker.append(temp_list)


      # self.axes = [figure.add_axes(rect, projection='polar', label='axes%d' % i) for i in range(self.n)]
      #
      # self.ax = self.axes[0]
      # self.ax.set_thetagrids(self.angles, labels=title, fontsize=14)

      # for ax in self.axes[1:]:
      #     ax.patch.set_visible(False)
      #     ax.grid(False)
      #     ax.xaxis.set_visible(False)

      # for ax, angle, label in zip(self.axes, self.angles, labels):
      #     ax.set_rgrids(range(1, AXES_DEPTH + 1), angle=angle, labels=label) # 6
      #     ax.spines['polar'].set_visible(False)
      #     ax.set_ylim(0, AXES_DEPTH + 1)

  def plot(self, values, *args, **kw):
      angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
      values = np.r_[values, values[0]]
      self.ax.plot(angle, values, *args, **kw)

if __name__ == '__main__':
    fig = plt.figure(figsize=(11, 11))

    # tit = [1,2,3,4,5, 6, 7, 8, 9,10,11] # 12x

    # lab = [
    #     [ 0 ,  15 ,  30 ,  45 ,  60 ,  75 ],
    #     [ 0 ,  -10 ,  -20 ,  -30 ,  -40 ,  -50 ],
    #     [ 0 ,  -20 ,  -40 ,  -60 ,  -80 ,  -100 ],
    #     [ 0 ,  -20 ,  -40 ,  -60 ,  -80 ,  -100 ],
    #     [ 0 ,  -6 ,  -12 ,  -18 ,  -24 ,  -30 ],
    #     [ 0 ,  - 14 ,  -28 ,  -42 ,  -56 ,  -70 ],
    #     [ 0 ,  250 ,  500 ,  750 ,  1000 ,  1250 ],
    #     [ 0 ,  3 ,  6 ,  9 ,  12 ,  15 ],
    #     [ 0 ,  50 ,  100 ,  150 ,  200 ,  250 ],
    #     [ 0 ,  -4 ,  -8 ,  -12 ,  -16 ,  -20 ],
    #     [ 0 ,  -6 ,  -12 ,  -18 ,  -24 ,  -30 ]
    # ]

    radar = Radar(fig, 'data.csv')
    # radar.plot([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #            ,  '-', lw=3, color='b', alpha=0.4, label='1')
    # radar.plot([4.60, 4.10, 5.45, 5.60, 4.83, 4.57, 4.78, 5.00, 4.78, 5.00, 4.83]
    #            , '-', lw=3, color='r', alpha=0.4, label='2')
    # radar.plot([4.60, 3.80, 5.45, 5.60, 3.83, 4.29, 5.01, 5.00, 4.94, 4.75, 4.33]
    #            , '-', lw=3, color='g', alpha=0.4, label='3')
    # radar.plot([4.60, 4.50, 5.45, 5.65, 5.83, 4.79, 4.55, 5.00, 4.62, 5.50, 5.17]
    #            , '-', lw=3, color='y', alpha=0.4, label='4')
    # radar.ax.legend()
    # plt.savefig('attempt.png', bbox_inches = 'tight', dpi = 500)
