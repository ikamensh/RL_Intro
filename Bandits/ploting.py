import matplotlib.pyplot as plt
from collections import deque

def plot_moving_avg(signal1D, x_axis_name, y_axis_name, plot_name, show=False, folder_path=None):

    plt.plot(moving_average(signal1D))

    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.title(plot_name)
    plt.grid(True)
    if folder_path is not None:
        print(folder_path+".png")
        plt.savefig(folder_path+".png")
    if show:
        plt.show()
    plt.clf()

def moving_average(signal1D):

    my_deque = deque(maxlen=7)
    averages=[]
    for value in signal1D:
        my_deque.append(value)
        averages.append(sum(my_deque)/len(my_deque))

    return averages

