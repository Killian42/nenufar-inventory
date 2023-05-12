"""
Author: Killian Lebreton, University of Orleans / LPC2E
Date: 2023-03 to 2023-08, Master 2 Internship
Description: This code creates a pdf of the timeline of
nenufar pulsar observations for every pulsar in the inventory
"""

### Libraries ###
from astropy.time import Time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
import glob
import os

### Data importation and preparation ###
file=glob.glob(os.getcwd() + "/pulsar-obs-inventory*.csv")[-1]
df = pd.read_csv(file, sep=";")
actual_psr_mask = (df["Pulsar name"].str[0]=="B") | (df["Pulsar name"].str[0]=="J")
df = df[actual_psr_mask]

df["obs_day_mjd"] = df["Filename"].str.split("_").str[2].astype(dtype=float)

mjd_formatted= Time(df["obs_day_mjd"], format="mjd")
df["obs_day_utc"] = mjd_formatted.datetime64

psrs = df["Pulsar name"]
unique_psrs = df["Pulsar name"].unique()
unique_psrs_sorted = unique_psrs[np.argsort(df["Pulsar name"].str[1:].unique())]

x_lims = (df["obs_day_mjd"].min()-100,df["obs_day_mjd"].max()+100)

def timeline_mkr(psr_arr,disp=False):
    fig = plt.figure(figsize=(12.4, 10.4))
    ax1 = fig.add_subplot()
    ax2 = ax1.twiny()
    colors = plt.rcParams["axes.prop_cycle"]()

    for i, psr in enumerate(psr_arr):
        mask = df["Pulsar name"] == psr
        sel = df[mask]
        ys = i * np.ones(len(sel))
        col = next(colors)["color"]

        ax1.text(
        df["obs_day_mjd"].min()-125,
        i,
        s=psr,
        c=col,
        fontsize=10,
        horizontalalignment="right",
        verticalalignment="center",
        zorder=5,
    )
        sc = ax1.scatter(
        sel["obs_day_mjd"],
        ys,
        c=col,
        marker="x",
        s=20,
        lw=1,
        zorder=5,
    )
        sc2 = ax2.scatter(
        sel["obs_day_utc"],
        ys,
        alpha=0,
    )
    
    ax1.grid()
    ax1.set_xlabel("MJD")
    ax1.set_ylabel("Pulsar name",labelpad=+75)
    ax1.set(yticklabels=[])
    ax1.tick_params(left=False)
    ax1.set_xlim(x_lims)
    ax1.set_ylim(-1, len(psr_arr) + 1)

    ax2.set_xlabel("UTC")

    plt.title("Nenufar pulsar observations timeline of " + psr_arr[-1] + " to " + psr_arr[0],pad=20,size=20)   

    pdf.savefig()  # saves the current figure into a pdf page  
    plt.close()

nb_of_arr = int(len(unique_psrs_sorted)/50)+1
split_arr = np.array_split(unique_psrs_sorted,nb_of_arr)

with PdfPages(os.getcwd() +'/obs_timeline.pdf') as pdf:
    for arr in split_arr:
        timeline_mkr(np.flip(arr))