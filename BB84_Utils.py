import pandas as pd
import numpy as np
from BB84_Protocol_v2 import simulate_bb84

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
        for repetition in repetition_r:                       # loop over all possible combinations of p and repetition times
            global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p, 0, seed, False)
            seed += L_init
            #safe data from simulation in Dataframe
            rows.append({
                "p": p,
                "repetition": repetition,
                "seed": seed,
                "global_R_miss": global_R_miss,
                "Z_R_miss": Z_R_miss,
                "X_R_miss": X_R_miss
            })

        seed+=1   # change seed for next run

    df = pd.DataFrame(rows)

    # compute the mean value of each experiment
    df_mean = df.groupby("p").agg(
        global_R_miss_mean=("global_R_miss", "mean"),
        Z_R_miss_mean=("Z_R_miss", "mean"),
        X_R_miss_mean=("X_R_miss", "mean")
    ).reset_index()
    return df_mean

#df = mismatch_ratio_experiment(False, False, False, 1, 300, np.arange(0,1.01,0.1), range(50))
#df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_ideal_50.csv", sep=';', index=False)
#print("ratio ideal done")