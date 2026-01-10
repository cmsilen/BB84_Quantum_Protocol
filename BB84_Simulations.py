import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from BB84_Utils import mismatch_ratio_experiment

# -------------DEFINING PARAMETER RANGES
# GLOBAL PARAMETERS
seed = 1  # initial seed
L_init = 300  # total exchanged bits
do_mismatch_experiments = True
do_undetected_experiments = False
do_false_positives = False
do_key_length_mismatch_experiments = False
do_key_length_undetected_experiments = False

# MISMATCH RATIO EXPERIMENT
p_r_mr = np.arange(0, 1.01, 0.1)  # probability of error in the quantum channel (same for bit- and phase-flip)
repetition_r_mr = range(10)  # times of experiment repetitions

# PROBABILITY OF UNDETECTED EAVESDROPPING EXPERIMENT
p_pu = 0.20
k_r_pi = np.arange(0.1, 1.01, 0.1)
repetition_r_pu = range(10000)

# EFFECTS OF KEY LENGTH VARIATIONS EXPERIMENT
L_init_r_lv = [700, 1000]

# safe plots in these folders
os.makedirs("results/mismatch_ratio_experiments", exist_ok=True)
os.makedirs("results/undetected_eavesdropping_experiments", exist_ok=True)
os.makedirs("results/L_init_experiments", exist_ok=True)

print('STARTING EXPERIMENTS...')

# ------------- MISMATCH RATIO EXPERIMENTS ---------------
if do_mismatch_experiments:
    # ideal channel conditions
    df = mismatch_ratio_experiment(False, False, False, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_ideal.csv", sep=';', index=False)
    print("ratio ideal done")

    # no eavesdropping, bit flip channel
    df = mismatch_ratio_experiment(False, True, False, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_bitflip.csv", sep=';', index=False)
    print("ratio no eavesdropping, bit flip done")

    # no eavesdropping, phase flip channel
    df = mismatch_ratio_experiment(False, False, True, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_phaseflip.csv", sep=';', index=False)
    print("ratio no eavesdropping, phase flip done")

    # no eavesdropping, bit and phase flip channel
    df = mismatch_ratio_experiment(False, True, True, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_bitphaseflip.csv", sep=';', index=False)
    print("ratio no eavesdropping, bit and phase flip done")

    # eavesdropping, no channel errors
    df = mismatch_ratio_experiment(True, False, False, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping.csv", sep=';', index=False)
    print("ratio eavesdropping, no channel errors done")

    # eavesdropping, bit flip channel
    df = mismatch_ratio_experiment(True, True, False, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping_bitflip.csv", sep=';', index=False)
    print("ratio eavesdropping, bit flip done")

    # eavesdropping, phase flip channel
    df = mismatch_ratio_experiment(True, False, True, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping_phaseflip.csv", sep=';', index=False)
    print("ratio eavesdropping, phase flip done")

    # eavesdropping, bit and phase flip channel
    df = mismatch_ratio_experiment(True, True, True, seed, L_init, p_r_mr, repetition_r_mr)
    df.to_csv("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping_bitphaseflip.csv", sep=';', index=False)
    print("ratio eavesdropping, bit and phase flip done")