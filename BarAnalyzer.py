import numpy as np
import pandas as pd
import pylab
from mpl_toolkits.mplot3d import Axes3D

days = 10  # days to show


def gradient(num):
    return 255 - np.random.randint(0, 255), 255 - np.random.randint(0, 255), num * 5


def show_BarGraph(file_stat, word_count):
    global days
    worksheet = pd.read_excel(file_stat, engine='openpyxl', index_col=0)
    if worksheet.empty:
        return False
    words = worksheet.loc[:, "word"].values.tolist()[:word_count]
    data = worksheet.iloc[:, 1:].values.tolist()[:word_count]
    data_zip = tuple(zip(*data))

    if len(data_zip) > days:
        days = len(data_zip)

    x = np.array(range(word_count))
    y = list(range(1, days + 1))
    z = data_zip[:]

    fig = pylab.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    clr = ['#{:02x}{:02x}{:02x}'.format(*gradient(i)) for i in range(word_count)]

    for i in range(1, days + 1):
        if i > len(data_zip):
            ax.bar(x, np.zeros(word_count), i, zdir='y', color=clr)
        else:
            ax.bar(x, z[i - 1], i, zdir='y', color=clr)

    ax.set_xticks(x)

    ax.set_xticklabels(words, size=5 + (50 - word_count) * 0.075, verticalalignment='bottom')
    x_ticklabels = ax.get_xticklabels()
    for j in range(len(x_ticklabels)):
        x_ticklabels[j].set_color(clr[j])

    ax.set_yticks(y)
    ax.set_xlabel('Слова')
    ax.set_ylabel('Дні')
    ax.set_zlabel('Кількість')
    fig.add_axes(ax)
    fig.canvas.set_window_title('Стовпчастий аналіз')
    pylab.show()
    return True
