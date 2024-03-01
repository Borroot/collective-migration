import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import json
from os import listdir

out_folder = 'arrow_output/'
in_folder = 'output/'
hist_folder = 'hist_output/'

# load the json file containing the results
with open(in_folder + 'results.json') as f:
    results = json.load(f)


def arrows():
    # construct the arrow images
    for experiment in results:
        for run in experiment['runs']:
            img = plt.imread(in_folder + run['img'])

            plt.figure(figsize=(7, 7))

            xy = np.array(run['xy'])
            dxy = np.array(run['dxy'])

            plt.quiver(xy[:, 0], 250 - xy[:, 1], dxy[:, 0], -dxy[:, 1], color='red')
            plt.scatter(xy[:, 0], 250 - xy[:, 1], color='red')

            plt.imshow(img, extent=(0, 250, 0, 250))

            plt.xlim(0, 250)
            plt.ylim(0, 250)

            plt.axis('off')

            plt.savefig(out_folder + run['img'])
            # plt.show()
            plt.clf()


def plot(angles, name, std):
    width = 1

    # plot the results
    plt.hist(angles, bins=30, density=True, label='samples')
    plt.vlines([-width * std, width * std], 0, 1, linestyles='--', color='red', label=f'$[-{width}\sigma, {width}\sigma]$ interval')

    plt.xlim([-np.pi, np.pi])
    plt.xlabel('direction angle in radians')
    plt.ylabel('probability density')

    plt.legend()
    plt.title(name + f' $\sigma = {std:.3f}$')

    plt.savefig(hist_folder + f'{name}.png')
    # plt.show()
    plt.clf()

    # plt the results polar
    ax = plt.subplot(projection='polar')

    plt.hist(angles, bins=30, density=True, label='samples')
    plt.vlines([-width * std, width * std], 0, 1, linestyles='--', color='red', label=f'$[-{width}\sigma, {width}\sigma]$ interval')

    plt.xlabel('direction angle in degrees')

    angle = np.deg2rad(67.5)
    plt.legend(loc='upper left', bbox_to_anchor=(.55 + np.cos(angle)/2, .63 + np.sin(angle)/2))
    plt.title(name + f' $\sigma = {std:.3f}$')

    plt.savefig(hist_folder + f'{name}_polar.png')
    # plt.show()
    plt.clf()


def angles():
    # quantify the collective migration
    for experiment in results:
        angles = []

        for run in experiment['runs']:
            dxy = np.array(run['dxy'])

            # compute all the angles
            new_angles = []
            for dx, dy in dxy:
                if dx == 0:
                    continue

                angle = np.tan(-dy / dx)
                if not np.isnan(angle):
                    new_angles.append(angle % (2 * np.pi))

            # compute the circular mean and shift the distribution to (0, 0)
            circmean = scipy.stats.circmean(new_angles)
            new_angles = [(angle - np.pi - circmean) % (2 * np.pi) - np.pi for angle in new_angles]

            angles += new_angles

        # compute the circular standard deviation
        std = scipy.stats.circstd(angles)

        # plot the results
        name = experiment['runs'][0]['img'].split('__', 1)[0]
        plot(angles, name, std)


if __name__ == '__main__':
    arrows()
    angles()