from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def show_MNK(file_stat, word):
    worksheet = pd.read_excel(file_stat, engine='openpyxl', index_col=0)
    values = worksheet.loc[worksheet['word'] == word].iloc[:, 1:].values.tolist()[0]
    n = len(values)
    if n < 20:
        return False
    koef = int(len(values) / 2)
    y_in = np.zeros((n, 1))
    F = np.ones((n, 3))

    for i in range(n):
        y_in[i, 0] = float(values[i])
        F[i, 1] = float(i)
        F[i, 2] = float(i * i)

    y_MNK = np.zeros(((n + koef), 1))
    f_t = F.T
    ff_t = f_t.dot(F)
    fft_i = np.linalg.inv(ff_t)
    ffti_ft = fft_i.dot(f_t)
    c = ffti_ft.dot(y_in)

    for i in range(n+koef):
        y_MNK[i, 0] = c[0, 0] + c[1, 0]*i + (c[2, 0]*i*i)
    plt.plot(y_in)
    plt.plot(y_MNK)
    plt.title('Аналіз слова "{}"'.format(word))
    plt.ylabel('Кількість повторень')
    plt.xlabel('Дні')
    fig_manager = plt.get_current_fig_manager()
    fig_manager.set_window_title('Графік аналізу МНК')
    width, height = fig_manager.window.maxsize()
    fig_manager.resize(int(width*0.75), int(height*0.8))
    fig_manager.window.wm_geometry("+0+20")
    x_ticks = list(range(n+koef))
    x_labels = list(range(1, n+koef+1))
    plt.xticks(ticks=x_ticks, labels=x_labels)
    plt.show()
    return True
