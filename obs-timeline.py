"""
Author: Killian Lebreton, University of Orleans / LPC2E
Date: 2023-03 to 2023-08, Master 2 Internship
Description: This code creates a pdf of the timeline of
nenufar pulsar observations for every pulsar in the inventory
"""

### Libraries ###
from astropy.time import Time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
import glob
import os
import argparse
import subprocess
from datetime import datetime,timedelta
matplotlib.rcParams["font.size"] = 17

### Argument parsing ###
def parse_args():
    """
    Parse the commandline arguments.

    Returns
    -------
    args: populated namespace
        The commandline arguments.
    """

    parser = argparse.ArgumentParser(
        description="Plot a timeline of NenuFAR observations",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-s",
        "--scope",
        dest="scope",
        type=str,
        choices=["all","thisweek"],
        default="all",
        help="Determine which observations are considered",
    )

    parser.add_argument(
        "-e",
        "--email",
        dest="email",
        type=str,
        nargs='+',
        default=None,
        help="Send the pdf file to this email adresss (or list of emails adresses).",
    )

    args = parser.parse_args()

    return args

args = parse_args()

### Data importation and preparation ###
file=glob.glob(os.getcwd() + "/pulsar-obs-inventory*.csv")[-1]
df = pd.read_csv(file, sep=";")
actual_psr_mask = (df["Pulsar name"].str[0]=="B") | (df["Pulsar name"].str[0]=="J")
df = df[actual_psr_mask]

if args.scope=='thisweek':
    today = datetime.now()
    lastweek = today-timedelta(7)
    lastweek_str =  lastweek.strftime("%Y-%m-%d")
    t=Time(lastweek_str, format='isot', scale='utc')
    cut_off = t.mjd

    mask = df["Filename"].str.split("_").str[2].astype(dtype=float) > cut_off

    df = df[mask]

    pad = 5.2
    x_lim_pad = 5
else:
    pad = 125
    x_lim_pad = 100

df["obs_day_mjd"] = df["Filename"].str.split("_").str[2].astype(dtype=float)

mjds = Time(df["obs_day_mjd"], format="mjd")
df["utc"] = mjds.datetime64

psrs = df["Pulsar name"]
unique_psrs = df["Pulsar name"].unique()
unique_psrs_sorted = unique_psrs[np.argsort(df["Pulsar name"].str[1:].unique())]

x0=df["obs_day_mjd"].min()-x_lim_pad
x1=df["obs_day_mjd"].max()+x_lim_pad
x_lims = (x0,x1)
x_lims_utc = ((Time(x0,format="mjd").datetime64,Time(x1,format="mjd").datetime64))

def timeline_mkr(psr_arr,disp=False,padding=pad):
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
        df["obs_day_mjd"].min()-padding,
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
        s=25,
        lw=1,
        zorder=5,
    )
        sc2 = ax2.scatter(
        sel["utc"],
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
    ax2.set_xlim(x_lims_utc)

    ax2.yaxis.set_major_locator(ticker.NullLocator())
    ax2.yaxis.set_minor_locator(ticker.NullLocator())

    locator = mdates.AutoDateLocator()
    ax2.xaxis.set_major_locator(locator)
    ax2.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    plt.xticks(rotation=10)

    plt.title("Nenufar pulsar observations timeline of " + psr_arr[-1] + " to " + psr_arr[0],pad=8,size=20)   

    pdf.savefig()  # saves the current figure into a pdf page  
    plt.close()

nb_of_arr = int(len(unique_psrs_sorted)/50)+1
split_arr = np.array_split(unique_psrs_sorted,nb_of_arr)

with PdfPages(os.getcwd() +'/obs_timeline_'+args.scope+'.pdf') as pdf:
    for arr in split_arr:
        timeline_mkr(np.flip(arr))

if args.email is not None:
    content = "This is an email your requested regarding NenuFAR pulsar observations. \n Please find attached a pdf with a timeline of these observations."
    subject = "NenuFAR pulsar observation timeline"
    attachment_path = os.getcwd() +'/obs_timeline_'+args.scope+'.pdf'
    recipients = args.email

    command = 'echo "{}" | mail -s "{}" -A {} {}'.format(content,subject, attachment_path, ','.join(recipients))
    subprocess.run(command,shell=True)