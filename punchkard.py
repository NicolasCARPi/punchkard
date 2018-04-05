#!/usr/bin/env python3
# plot punch card for repos
# see https://developer.github.com/v3/repos/statistics/#get-the-number-of-commits-per-hour-in-each-day
import numpy as np
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import requests
from os import getenv

# CONFIG
# list of repos to plot
repos = ['neovim/neovim', 'vim/vim', 'git/git', 'microsoft/vscode', 'elabftw/elabftw', 'google/protobuf']
# what is the env var with the github token
TOKEN_NAME='GITHUB_TOKEN'
# see https://matplotlib.org/examples/color/colormaps_reference.html for list
COLOR_MAP='hot'
# END CONFIG

def getToken():
    """
        Get token from env
    """
    token = getenv(TOKEN_NAME)
    if token == None:
        raise SystemExit('No token found. Use env variable %s' % TOKEN_NAME)
    return token

def getJson(repo):
    """
        Get punch card json for a repo
    """

    url='https://api.github.com/repos/' + repo + '/stats/punch_card'
    r = requests.get(url, headers={'Authorization': 'token %s' % getToken()})
    if r.status_code == 403:
        raise SystemExit('Rate limited!')
    return r.json()

def makeImg(json):
    """
        Create a 2d numpy array holding the number of commits
        x is the time of day
        y is the day of week
    """

    img = np.zeros((7, 24), dtype=int)

    for entry in json:
        img[entry[0], entry[1]] = entry[2]

    return img

def makeFigure(imgList):
    """
        Create a figure for all the images we have
    """
    for i, img in enumerate(imgList):
        i += 1
        ax = plt.subplot(len(imgList), 1, i)
        ax.imshow(img[0], cmap=COLOR_MAP)
        ax.get_yaxis().set_ticks([])
        if i == len(imgList):
            ax.set_xlabel('Time of day')
        ax.set_ylabel('Day of week')
        # add name of the repo as title
        plt.title(img[1])

    plt.tight_layout(pad=0)
    plt.show()

# START OF SCRIPT
imgList = []

for repo in repos:
    json = getJson(repo)
    # add a tuple to the list with the image and also the name of the repo
    imgList.append((makeImg(json), repo))

makeFigure(imgList)
