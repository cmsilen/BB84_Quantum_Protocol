import pandas as pd
import numpy as np
from BB84_Protocol_v2 import simulate_bb84
from scipy.stats import norm


def mismatch_ratio_experiment(eavesdropping_event, bit_flip_event, phase_flip_event, seed, L_init, p_r, repetition_r):
    # save intermediate results
    df = pd.DataFrame(columns=[
        "p",
        "repetition",
        "seed",
        "global_R_miss",
        "Z_R_miss",
        "X_R_miss"
    ])
    rows = []

    # starting experiments
    for p in p_r:
        for repetition in repetition_r:  # loop over all possible combinations of p and repetition times
            global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event,
                                                                            phase_flip_event, p, 0, seed)

            # safe data from simulation in Dataframe
            rows.append({
                "p": p,
                "repetition": repetition,
                "seed": seed,
                "global_R_miss": global_R_miss,
                "Z_R_miss": Z_R_miss,
                "X_R_miss": X_R_miss
            })
            seed += L_init  # change seed for next run

    df = pd.DataFrame(rows)

    # compute the mean value of each experiment
    df_mean = df.groupby("p").agg(
        global_R_miss_mean=("global_R_miss", "mean"),
        Z_R_miss_mean=("Z_R_miss", "mean"),
        X_R_miss_mean=("X_R_miss", "mean")
    ).reset_index()

    # calculate the upper and lower value for confidence intervall
    alpha = 0.01  # set value for alpha -> for 99% CI
    n = len(df_mean)
    z = norm.ppf(1 - alpha / 2)

    cols = ["global_R_miss", "Z_R_miss", "X_R_miss"]
    df_std = df.groupby("p")[["global_R_miss", "Z_R_miss", "X_R_miss"]].std()
    sem = df_std[cols].to_numpy() / np.sqrt(n)

    # Half-width of 99%-CI
    hw = z * sem

    # Lower/Upper CI
    df_mean[[c + "_lower" for c in cols]] = -hw
    df_mean[[c + "_upper" for c in cols]] = hw

    return df_mean


def probability_undetected_experiment(eavesdropping_event, bit_flip_event, phase_flip_event, seed, L_init, p_pu, k_r,
                                      repetition_r):
    # save intermediate results
    df = pd.DataFrame(columns=[
        "p",
        "k",
        "repetition",
        "seed",
        "undetected"
    ])

    rows = []

    # starting experiments
    for k in k_r:
        for repetition in repetition_r:  # loop over all possible combinations of p and repetition times
            global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event,
                                                                            phase_flip_event, p_pu, k, seed)

            # safe data from simulation in Dataframe
            rows.append({
                "p": p_pu,
                "k": k,
                "repetition": repetition,
                "seed": seed,
                "undetected": int(not eve_detected)
            })
            seed += L_init  # change seed for next run

    df = pd.DataFrame(rows)

    # probability by averaging the amount of 0 and 1 in detected column
    df_mean = df.groupby("k").agg(
        undetected_mean=("undetected", "mean")
    ).reset_index()

    alpha = 0.01  # set value for alpha -> for 99% certainty
    n = len(df_mean)
    z = norm.ppf(1 - alpha / 2)

    df_std = df.groupby("k")[["undetected"]].std()
    sem = df_std["undetected"].to_numpy() / np.sqrt(n)

    # Half-width of 99%-CI
    hw = z * sem

    # Lower/Upper CI
    df_mean["undetected_lower"] = -hw
    df_mean["undetected_upper"] = hw

    return df_mean


