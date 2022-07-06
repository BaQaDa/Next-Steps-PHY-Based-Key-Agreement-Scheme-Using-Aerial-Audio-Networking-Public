# source for this plot is
# https://www.pythoncharts.com/matplotlib/beautiful-bar-charts-matplotlib/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# df = pd.DataFrame({
#     'year':[2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
#     'no.users':[3668, 4435, 5095, 5643, 6055, 6378, 6648, 6925, 7138, 7336, 7516],
# })
df = pd.DataFrame({
    'year':['2016', '2017', '2018', '2019', '2020', '2021', '2022*', '2023*', '2024*', '2025*', '2026*'],
    'no.users':[3668, 4435, 5095, 5643, 6055, 6378, 6648, 6925, 7138, 7336, 7516],
})
print (df)
# ___________________________________________________________________________________________________
#                                  1. Create our first bar chart.
# ---------------------------------------------------------------------------------------------------
# plt.subplots(figsize=(8, 5))
# # Plot the bar graph
# plot = plt.bar(x= df['year'], height= df['no.users'])
# # Display the graph on the screen
#
# plt.show()
# ___________________________________________________________________________________________________
#                                  2. Create a high-resolution chart.
# ---------------------------------------------------------------------------------------------------
# # Increase the quality and resolution of our charts so we can copy/paste or just
# # directly save from here.
# # See:
# # https://ipython.org/ipython-doc/3/api/generated/IPython.display.html
# from IPython.display import set_matplotlib_formats
# set_matplotlib_formats('retina', quality=100)
#
# # You can also just do this in Colab/Jupyter, some "magic":
# # %config InlineBackend.figure_format='retina'
#
# # Set default figure size.
# plt.rcParams['figure.figsize'] = (8, 5)
# fig, ax = plt.subplots()
#
# ax.bar(df['year'], df['no.users'])
#
# # Make the chart fill out the figure better.
# fig.tight_layout()
# plt.show()
# ___________________________________________________________________________________________________
#                                  3. Simple Axes: remove unnecessary lines
# ---------------------------------------------------------------------------------------------------
# fig, ax = plt.subplots()
#
# ax.bar(df['year'], df['no.users'])
#
# # First, let's remove the top, right and left spines (figure borders)
# # which really aren't necessary for a bar chart.
# # Also, make the bottom spine gray instead of black.
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['bottom'].set_color('#DDDDDD')
#
# # Second, remove the ticks as well.
# ax.tick_params(bottom=False, left=False)
#
# # Third, add a horizontal grid (but keep the vertical grid hidden).
# # Color the lines a light gray as well.
# ax.set_axisbelow(True)
# ax.yaxis.grid(True, color='#EEEEEE')
# ax.xaxis.grid(False)
#
# fig.tight_layout()
# plt.show()

# ___________________________________________________________________________________________________
#                                  4. Adding text annotations
# ---------------------------------------------------------------------------------------------------
# fig, ax = plt.subplots()
#
# # Save the chart so we can loop through the bars below.
# bars = ax.bar(df['year'], df['no.users'])
#
# # Axis formatting.
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['bottom'].set_color('#DDDDDD')
# ax.tick_params(bottom=False, left=False)
# ax.set_axisbelow(True)
# ax.yaxis.grid(True, color='#EEEEEE')
# ax.xaxis.grid(False)
#
# # Grab the color of the bars so we can make the
# # text the same color.
# bar_color = bars[0].get_facecolor()
#
# # Add text annotations to the top of the bars.
# # Note, you'll have to adjust this slightly (the 0.3)
# # with different data.
# for bar in bars:
#   ax.text(
#       bar.get_x() + bar.get_width() / 2,
#       bar.get_height() + 0.3,
#       round(bar.get_height(), 1),
#       horizontalalignment='center',
#       color=bar_color,
#       weight='bold'
#   )
#
# fig.tight_layout()
# fig.tight_layout()
# plt.show()

# ___________________________________________________________________________________________________
#                                  5. Finishing Touches: add nicely formatted labels and title
# ---------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

# Save the chart so we can loop through the bars below.
# plt.subplots(figsize=(8, 5))

bars = ax.bar(df['year'], df['no.users'])

# Axis formatting.
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)

# Add text annotations to the top of the bars.
bar_color = bars[0].get_facecolor()
for bar in bars:
  ax.text(
      bar.get_x() + bar.get_width() / 2,
      bar.get_height() + 30,
      round(bar.get_height(), 1),
      horizontalalignment='center',
      color=bar_color,
      weight='bold'
  )

# Add labels and a title. Note the use of `labelpad` and `pad` to add some
# extra space between the text and the tick labels.
ax.set_xlabel('Year', labelpad=15, color='#333333', )
ax.set_ylabel('Smartphone users in millions', labelpad=15, color='#333333')
# ax.set_title('Number of smartphone users worldwide from 2016 to 2026 (in millions)', pad=15, color='#333333')

plt.tight_layout()
# plt.figure(dpi=150)
plt.savefig("statistic-smartphone-users-worldwide-2016-2026", dpi=1000)
plt.show()
