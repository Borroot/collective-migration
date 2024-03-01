import numpy as np
import matplotlib.pyplot as plt

from os import listdir

folder = 'output/'
files = sorted([f for f in listdir(folder) if not 'final' in f])

for i in range(0, len(files), 2):
    Xs = np.genfromtxt(folder + files[i + 1], delimiter=",")
    img = plt.imread(folder + files[i])

    plt.figure(figsize=(7, 7))

    plt.quiver(Xs[:, 0], 250 - Xs[:, 1], Xs[:, 2], -Xs[:, 3], color='red')
    plt.scatter(Xs[:, 0], 250 - Xs[:, 1], color='red')

    plt.imshow(img, extent=(0, 250, 0, 250))

    plt.xlim(0, 250)
    plt.ylim(0, 250)

    plt.axis('off')

    plt.savefig(folder + 'final_' + files[i])
    # plt.show()
