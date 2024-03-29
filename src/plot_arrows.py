import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import json
from os import listdir

out_folder = 'arrow_output/'
in_folder = 'output/'

# load the json file containing the results
with open(in_folder + 'results.json') as f:
    results = json.load(f)


def arrows():
    # construct the arrow images
    for experiment in results:
        for run in experiment['runs']:
            try:
                img = plt.imread(in_folder + run['img'])
            except:
                print(in_folder + run['img'], 'not found')
                continue

            plt.figure(figsize=(7, 7))

            xy = np.array(run['xy'])
            dxy = np.array(run['dxy'])

            plt.quiver(xy[:, 0], 250 - xy[:, 1], dxy[:, 0], -dxy[:, 1], color='red')
            plt.scatter(xy[:, 0], 250 - xy[:, 1], color='red')

            plt.imshow(img, extent=(0, 250, 0, 250))

            plt.xlim(0, 250)
            plt.ylim(0, 250)

            plt.axis('off')
            plt.savefig(out_folder + run['img'], bbox_inches="tight", dpi=300)
            # plt.show()
            plt.clf()



if __name__ == '__main__':
    arrows()
