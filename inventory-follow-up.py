"""
Author: Killian Lebreton, University of Orleans / LPC2E
Date: 2023-03 to 2023-08, Master 2 Internship
Description: This code creates a csv file containing basic information
on pulsars observed by the nenufar telescope, along with the number and
duration of these observations
"""

### Librairies ###
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psrqpy
import warnings
import os
import glob

warnings.filterwarnings("error")

### Data importation ###
inv_files=glob.glob(os.getcwd() + "/pulsar-obs-inventory*.csv")

df = pd.read_csv(inv_files[-1], sep=";")

obs_duration = df["Observation duration (s)"].to_numpy(dtype=float)
mode = df["Mode"].to_numpy(dtype=str)
psr = df["Pulsar name"].to_numpy(dtype=str)
filenames = df["Filename"].to_numpy(dtype=str)

### Data preparation ###
not_psr_idx = []
for i, p in enumerate(psr):
    if p[0] == "B" or p[0] == "J":
        pass
    else:
        not_psr_idx.append(i)

not_psr = psr[not_psr_idx]
unique_not_psr, unique_not_psr_idx = np.unique(not_psr, return_index=True)

unique_psr, unique_psr_idx = np.unique(np.delete(psr, not_psr_idx), return_index=True)

PSR_mode_mask = mode == "PSR"
SEARCH_mode_mask = mode == "SEARCH"

### PSR parameters ###
## Fetching ##
df = psrqpy.QueryATNF(
    psrs=unique_psr[0],
    params=["Name", "JName", "RAJ", "DecJ", "P0", "DM", "RM"],
    include_errs=False,
    sort_attr="Jname",
    checkupdate=True,
).dataframe
for p in unique_psr[1:]:
    try:  # looks up the psr in the catalogue
        q = psrqpy.QueryATNF(
            psrs=p,
            params=["Name", "JName", "RAJ", "DecJ", "P0", "DM", "RM"],
            include_errs=False,
            sort_attr="Jname",
        )
        df_temp = q.dataframe
        df = pd.concat([df, df_temp], ignore_index=True, sort=True)

    except:  # if the psr is not in the catalogue, sets dummy values for the parameters. Will be replaced by looking at the values in the par file of the observation in the future
        df_temp = pd.DataFrame(
            {
                "NAME": [p],
                "JNAME": ["Not in catalogue"],
                "RAJ": ["0"],
                "DECJ": ["0"],
                "P0": [0],
                "DM": [0],
                "RM": [0],
            }
        )
        df = pd.concat([df, df_temp], ignore_index=True, sort=True)

## Renaming and reordering ##
psr_param_header = [
    "Name",
    "JName",
    "RAJ (hms)",
    "DecJ (dms)",
    "P0 (s)",
    "DM (pc/cm^3)",
    "RM (rad/m^2)",
]

df = df.reindex(sorted(df.columns), axis=1)
df = df.rename(
    columns={
        "RAJ": "RAJ (hms)",
        "DECJ": "DecJ (dms)",
        "P0": "P0 (s)",
        "DM": "DM (pc/cm^3)",
        "RM": "RM (rad/m^2)",
        "NAME": "Name",
        "JNAME": "JName",
    }
)
df = df[psr_param_header]


### Useful observation info computation ###
def obs_time_comp(obs_duration_arr, unique_psr_arr, unique_psr_idx_arr):
    obs_time = np.zeros_like(unique_psr_idx_arr, dtype=float)
    file_nb = np.zeros_like(unique_psr_idx_arr, dtype=int)

    for i in range(len(unique_psr_arr)):
        obs_lst = []
        if i == len(unique_psr_arr) - 1:
            obs_time_arr = obs_duration_arr[unique_psr_idx_arr[i] :]
            obs_time[i] = np.sum(obs_time_arr)

        else:
            obs_time_arr = obs_duration_arr[
                unique_psr_idx_arr[i] : unique_psr_idx_arr[i + 1]
            ]
            obs_time[i] = np.sum(obs_time_arr)

        file_nb[i] += len(obs_time_arr)

    return obs_time, file_nb


def uniq_obs_counter(psr_arr, files_arr):
    uniq_psr_arr, idx = np.unique(psr_arr, return_index=True)
    cpt = np.zeros_like(uniq_psr_arr, dtype=int)

    for i, p in enumerate(uniq_psr_arr):
        ii = idx[i]
        obs_lst = []
        while psr_arr[ii] == p:
            obs = files_arr[ii].split("_")[1]
            if obs in obs_lst:
                pass
            else:
                obs_lst.append(obs)

            if ii < len(psr_arr) - 1:
                ii += 1
            else:
                break
        cpt[i] = len(obs_lst)

    return cpt


## Number of observations ##
SEARCH_unique_obs_nb = uniq_obs_counter(
    psr[SEARCH_mode_mask], filenames[SEARCH_mode_mask]
)

PSR_unique_obs_nb = uniq_obs_counter(psr[PSR_mode_mask], filenames[PSR_mode_mask])

## Length of the observations ##

SEARCH_unique_psr, SEARCH_unique_psr_idx = np.unique(
    psr[SEARCH_mode_mask], return_index=True
)
SEARCH_obs_time, SEARCH_file_nb = obs_time_comp(
    obs_duration[SEARCH_mode_mask], SEARCH_unique_psr, SEARCH_unique_psr_idx
)

PSR_unique_psr, PSR_unique_psr_idx = np.unique(psr[PSR_mode_mask], return_index=True)
PSR_obs_time, PSR_file_nb = obs_time_comp(
    obs_duration[PSR_mode_mask], PSR_unique_psr, PSR_unique_psr_idx
)

### Preparation for saving ###
## SEARCH mode ##

SEARCH_obs_time_sum = np.zeros_like(unique_psr, dtype=float)
SEARCH_file_nb_full = np.zeros_like(unique_psr, dtype=int)
SEARCH_unique_obs_nb_full = np.zeros_like(unique_psr, dtype=int)

for i, v in enumerate(unique_psr):
    for ii, vv in enumerate(SEARCH_unique_psr):
        if v == vv:
            SEARCH_obs_time_sum[i] = SEARCH_obs_time[ii]
            SEARCH_file_nb_full[i] = SEARCH_file_nb[ii]
            SEARCH_unique_obs_nb_full[i] = SEARCH_unique_obs_nb[ii]
        else:
            pass

## PSR Mode ##
PSR_obs_time_sum = np.zeros_like(unique_psr, dtype=float)
PSR_file_nb_full = np.zeros_like(unique_psr, dtype=int)
PSR_unique_obs_nb_full = np.zeros_like(unique_psr, dtype=int)

for i, v in enumerate(unique_psr):
    for ii, vv in enumerate(PSR_unique_psr):
        if v == vv:
            PSR_obs_time_sum[i] = PSR_obs_time[ii]
            PSR_file_nb_full[i] = PSR_file_nb[ii]
            PSR_unique_obs_nb_full[i] = PSR_unique_obs_nb[ii]
        else:
            pass

## Adding the computed info to the main dataframe ##
df.insert(7, "N_file in PSR", PSR_file_nb_full)

df.insert(8, "N_file in SEARCH", SEARCH_file_nb_full)

df.insert(9, "N_obs in PSR", PSR_unique_obs_nb_full)

df.insert(10, "N_obs in SEARCH", PSR_unique_obs_nb_full)

df.insert(11, "T_obs in PSR (s)", PSR_obs_time_sum)

df.insert(12, "T_obs in SEARCH (s)", SEARCH_obs_time_sum)

## Handling the non-pulsar files ## ["Name","JName","RAJ (hms)","DecJ (dms)","P0 (s)","DM (pc/cm^3)","RM (rad/m^2)"]
for i, v in enumerate(not_psr):
    df_temp = pd.DataFrame(
        {
            "Name": [v],
            "JName": ["Not a psr / Check par file"],
            "RAJ (hms)": ["0"],
            "DecJ (dms)": ["0"],
            "P0 (s)": [0],
            "DM (pc/cm^3)": [0],
            "RM (rad/m^2)": [0],
            "N_file in PSR": [0],
            "N_file in SEARCH": [0],
            "N_obs in PSR": [0],
            "N_obs in SEARCH": [0],
            "T_obs in PSR (s)": [0],
            "T_obs in SEARCH (s)": [0],
        }
    )
    df = pd.concat([df, df_temp], ignore_index=True)

### File saving ###
filename = "psr_info.csv"

df.to_csv(filename, sep=";", index=False)


#test comment