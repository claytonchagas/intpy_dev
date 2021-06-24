import os
import time
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import imageio


def draw(matrix):
    ax = sns.heatmap(matrix, cmap="coolwarm")
    if not os.path.exists("images/tmp"):
        os.makedirs("images/tmp")
    plt.savefig("images/tmp/img_" + str(time.time()) + ".png")
    plt.close()
    #plt.show()


def generateGif():
    directory = "images/tmp/"
    if not os.path.exists("images/gif"):
        os.makedirs("images/gif")
    with imageio.get_writer('images/gif/movie.gif', mode='I', duration=0.5) as writer:
        for filename in sorted(os.listdir(directory)):
            image = imageio.imread(directory + filename)
            writer.append_data(image)
    writer.close()
    clearFiles(directory)


def clearFiles(directory):
    if os.path.exists(directory):
        files = os.listdir(directory)
        for filename in files:
            os.remove(os.path.join(directory, filename))
