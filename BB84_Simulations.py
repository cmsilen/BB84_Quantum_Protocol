import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from BB84_Utils import mismatch_ratio_experiment
from BB84_Utils import probability_undetected_experiment

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
repetition_r_mr = range(100)  # times of experiment repetitions

# PROBABILITY OF UNDETECTED EAVESDROPPING EXPERIMENT
p_pu = 0.20  # probability of error in the quantum channel -> fixed
k_r_pu = np.arange(0.1, 1.01, 0.1)  # fraction of the disclosed quantum key for eavesdropping detection
repetition_r_pu = range(4)  # how many times an experiment is repeated

# EFFECTS OF KEY LENGTH VARIATIONS EXPERIMENT
L_init_r_lv = [100, 300, 700, 1000]  # four cases for different L_init lengths

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

# ----- UNDETECTED EAVESDROPPING EXPERIMENTS -----
if do_undetected_experiments:
    # ideal conditions
    df = probability_undetected_experiment(True, False, False, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    df.to_csv("results/undetected_eavesdropping_experiments/probability_undetected_ideal.csv", sep=';', index=False)
    print("P_und ideal done")

    # bit flip channel
    df = probability_undetected_experiment(True, True, False, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    df.to_csv("results/undetected_eavesdropping_experiments/probability_undetected_bitflip.csv", sep=';', index=False)
    print("P_und bit flip done")

    # phase flip channel
    df = probability_undetected_experiment(True, False, True, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    df.to_csv("results/undetected_eavesdropping_experiments/probability_undetected_phaseflip.csv", sep=';', index=False)
    print("P_und phase flip done")

    # bit and phase flip channel
    df = probability_undetected_experiment(True, True, True, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    df.to_csv("results/undetected_eavesdropping_experiments/probability_undetected_bitphaseflip.csv", sep=';',
              index=False)
    print("P_und bit and phase flip done")

# ----- EFFECTS OF L_init VARIATION -----
for (L_init_lv) in L_init_r_lv:
    print("Start L_init variation experiments. L_init: ", L_init_lv)
    if do_key_length_mismatch_experiments:
        # MISMATCH RATIO EXPERIMENTS
        # ideal channel conditions
        df = mismatch_ratio_experiment(False, False, False, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_ideal_{L_init_lv}.csv", sep=';', index=False)
        print("ratio ideal done")

        # no eavesdropping, bit flip channel
        df = mismatch_ratio_experiment(False, True, False, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_bitflip_{L_init_lv}.csv", sep=';', index=False)
        print("ratio no eavesdropping, bit flip done")

        # no eavesdropping, phase flip channel
        df = mismatch_ratio_experiment(False, False, True, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_phaseflip_{L_init_lv}.csv", sep=';', index=False)
        print("ratio no eavesdropping, phase flip done")

        # no eavesdropping, bit and phase flip channel
        df = mismatch_ratio_experiment(False, True, True, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_bitphaseflip_{L_init_lv}.csv", sep=';', index=False)
        print("ratio no eavesdropping, bit and phase flip done")

        # eavesdropping, no channel errors
        df = mismatch_ratio_experiment(True, False, False, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_eavesdropping_bitflip_{L_init_lv}.csv", sep=';',
                  index=False)
        print("ratio eavesdropping, no channel errors done")

        # eavesdropping, bit flip channel
        df = mismatch_ratio_experiment(True, True, False, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_eavesdropping_phaseflip_{L_init_lv}.csv", sep=';',
                  index=False)
        print("ratio eavesdropping, bit flip done")

        # eavesdropping, phase flip channel
        df = mismatch_ratio_experiment(True, False, True, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_eavesdropping_bitphaseflip_{L_init_lv}.csv", sep=';',
                  index=False)
        print("ratio eavesdropping, phase flip done")

        # eavesdropping, bit and phase flip channel
        df = mismatch_ratio_experiment(True, True, True, seed, L_init_lv, p_r_mr, repetition_r_mr)
        df.to_csv(f"results/L_init_experiments/mismatch_ratios_ideal_{L_init_lv}.csv", sep=';', index=False)
        print("ratio eavesdropping, bit and phase flip done")

    if do_key_length_undetected_experiments:
        # ideal conditions
        df = probability_undetected_experiment(True, False, False, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        df.to_csv(f"results/undetected_eavesdropping_experiments/probability_undetected_ideal_{L_init_lv}.csv", sep=';',
                  index=False)
        print("P_und ideal done")

        # bit flip channel
        df = probability_undetected_experiment(True, True, False, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        df.to_csv(f"results/undetected_eavesdropping_experiments/probability_undetected_bitflip_{L_init_lv}.csv",
                  sep=';', index=False)
        print("P_und bit flip done")

        # phase flip channel
        df = probability_undetected_experiment(True, False, True, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        df.to_csv(f"results/undetected_eavesdropping_experiments/probability_undetected_phaseflip_{L_init_lv}.csv",
                  sep=';', index=False)
        print("P_und phase flip done")

        # bit and phase flip channel
        df = probability_undetected_experiment(True, True, True, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        df.to_csv(f"results/undetected_eavesdropping_experiments/probability_undetected_bitphaseflip_{L_init_lv}.csv",
                  sep=';', index=False)
        print("P_und bit and phase flip done")
