import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# Configs
# =========================
CSV_PATH_MISMATCH = "results/mismatch_ratio_experiments"
CSV_PATH_UNDETECTED = "results/undetected_eavesdropping_experiments"
CSV_PATH_LINIT = "results/L_init_experiments"
SAVE_PATH = "plots"
os.makedirs(SAVE_PATH, exist_ok=True)

do_mismatch = True
do_undetected = True
do_Linit = False

MISMATCH_LABELS = [
    "ideal",
    "bit flip",
    "phase flip",
    "bit-phase flip"
]
UNDETECTED_LABELS = [
    "ideal",
    "bit flip",
    "phase flip",
    "bit-phase flip"
]
MISMATCH_LINIT_LABELS = [
    "L_init = 100",
    "L_init = 300",
    "L_init = 700",
    "L_init = 1000"
]
UNDETECTED_LINIT_LABELS = [
    "L_init = 100",
    "L_init = 300",
    "L_init = 700",
    "L_init = 1000"
]

CSVS_MISMATCH_NOEAVESDROPPING = [
    "mismatch_ratios_ideal.csv",
    "mismatch_ratios_bitflip.csv",
    "mismatch_ratios_phaseflip.csv",
    "mismatch_ratios_bitphaseflip.csv"
]
CSVS_MISMATCH_EAVESDROPPING = [
    "mismatch_ratios_eavesdropping.csv",
    "mismatch_ratios_eavesdropping_bitflip.csv",
    "mismatch_ratios_eavesdropping_phaseflip.csv",
    "mismatch_ratios_eavesdropping_bitphaseflip.csv"
]
CSVS_UNDETECTED = [
    "probability_undetected_ideal.csv",
    "probability_undetected_bitflip.csv",
    "probability_undetected_phaseflip.csv",
    "probability_undetected_bitphaseflip.csv"
]
CSVS_LINIT_MISMATCH = [
    "mismatch_ratios_bitphaseflip_100.csv",
    "mismatch_ratios_bitphaseflip_300.csv",
    "mismatch_ratios_bitphaseflip_700.csv",
    "mismatch_ratios_bitphaseflip_1000.csv"
]
CSVS_LINIT_UNDETECTED = [
    "probability_undetected_ideal_100.csv",
    "probability_undetected_bitflip_300.csv",
    "probability_undetected_phaseflip_700.csv",
    "probability_undetected_bitphaseflip_1000.csv"
]

ALPHA = 0.25                  # trasparenza banda

df_array_mismatch_noeavesdropping = []
if do_mismatch:
    for csv in CSVS_MISMATCH_NOEAVESDROPPING:
        df = pd.read_csv(f"{CSV_PATH_MISMATCH}/{csv}", sep=";")
        df_array_mismatch_noeavesdropping.append(df)

df_array_mismatch_eavesdropping = []
if do_mismatch:
    for csv in CSVS_MISMATCH_EAVESDROPPING:
        df = pd.read_csv(f"{CSV_PATH_MISMATCH}/{csv}", sep=";")
        df_array_mismatch_eavesdropping.append(df)

df_array_undetected = []
if do_undetected:
    for csv in CSVS_UNDETECTED:
        df = pd.read_csv(f"{CSV_PATH_UNDETECTED}/{csv}", sep=";")
        df_array_undetected.append(df)

df_array_mismatch_L_init = []
if do_Linit:
    for csv in CSVS_LINIT_MISMATCH:
        df = pd.read_csv(f"{CSV_PATH_LINIT}/{csv}", sep=";")
        df_array_mismatch_L_init.append(df)

df_array_undetected_L_init = []
if do_Linit:
    for csv in CSVS_LINIT_UNDETECTED:
        df = pd.read_csv(f"{CSV_PATH_LINIT}/{csv}", sep=";")
        df_array_undetected_L_init.append(df)

# =========================
# Funzione di plotting
# =========================
def plot_ci(df_array, x_name, mean_name, low_name, high_name, x_label, y_label, labels, filename):
    plt.figure(figsize=(6, 4))

    for i in range(len(df_array)):
        df = df_array[i]
        x = df[x_name].astype(float).to_numpy()
        mean = df[mean_name].astype(float).to_numpy()
        low = df[low_name].astype(float).to_numpy()
        high = df[high_name].astype(float).to_numpy()

        plt.errorbar(x, mean, yerr=high, markersize=2, fmt="o-", capsize=3, label=labels[i])

        print(f"\nCurve {labels[i]}")
        print("x:", x[:3])
        print("mean:", mean[:3])
        print("low:", low[:3])
        print("high:", high[:3])
        print("any high < low:", np.any(high < low))
        print("any NaN:", np.isnan(low).any(), np.isnan(high).any())

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# =========================
# Global no eavesdropping
# =========================
plot_ci(
    df_array_mismatch_noeavesdropping,
    "p",
    "global_R_miss_mean",
    "global_R_miss_lower",
    "global_R_miss_upper",
    "Channel error probability",
    "Global mismatch",
    MISMATCH_LABELS,
    f"{SAVE_PATH}/mismatch_noeavesdropping_global.png",
)

# =========================
# Z basis no eavesdropping
# =========================
plot_ci(
    df_array_mismatch_noeavesdropping,
    "p",
    "Z_R_miss_mean",
    "Z_R_miss_lower",
    "Z_R_miss_upper",
    "Channel error probability",
    "Z basis mismatch",
    MISMATCH_LABELS,
    f"{SAVE_PATH}/mismatch_noeavesdropping_Z.png",
)

# =========================
# X basis no eavesdropping
# =========================
plot_ci(
    df_array_mismatch_noeavesdropping,
    "p",
    "X_R_miss_mean",
    "X_R_miss_lower",
    "X_R_miss_upper",
    "Channel error probability",
    "X basis mismatch",
    MISMATCH_LABELS,
    f"{SAVE_PATH}/mismatch_noeavesdropping_X.png",
)

# =========================
# Global eavesdropping
# =========================
plot_ci(
    df_array_mismatch_eavesdropping,
    "p",
    "global_R_miss_mean",
    "global_R_miss_lower",
    "global_R_miss_upper",
    "Channel error probability",
    "Global mismatch",
    MISMATCH_LABELS,
    f"{SAVE_PATH}/mismatch_eavesdropping_global.png",
)

# =========================
# Z basis eavesdropping
# =========================
plot_ci(
    df_array_mismatch_eavesdropping,
    "p",
    "Z_R_miss_mean",
    "Z_R_miss_lower",
    "Z_R_miss_upper",
    "Channel error probability",
    "Z basis mismatch",
    MISMATCH_LABELS,
    f"{SAVE_PATH}/mismatch_eavesdropping_Z.png",
)

# =========================
# X basis eavesdropping
# =========================
plot_ci(
    df_array_mismatch_eavesdropping,
    "p",
    "X_R_miss_mean",
    "X_R_miss_lower",
    "X_R_miss_upper",
    "Channel error probability",
    "X basis mismatch",
    MISMATCH_LABELS,
    f"{SAVE_PATH}/mismatch_eavesdropping_X.png",
)

# =========================
# Undetected probability
# =========================
plot_ci(
    df_array_undetected,
    "k",
    "undetected_mean",
    "undetected_lower",
    "undetected_upper",
    "Fraction of the disclosed key",
    "Probability of undetected eavesdropping",
    UNDETECTED_LABELS,
    f"{SAVE_PATH}/undetected.png",
)

# =========================
# Global eavesdropping L_init variations
# =========================
plot_ci(
    df_array_mismatch_L_init,
    "p",
    "global_R_miss_mean",
    "global_R_miss_lower",
    "global_R_miss_upper",
    "Channel error probability",
    "Global mismatch",
    MISMATCH_LINIT_LABELS,
    f"{SAVE_PATH}/mismatch_L_init_eavesdropping_global.png",
)

# =========================
# Undetected eavesdropping L_init variations
# =========================
plot_ci(
    df_array_undetected_L_init,
    "k",
    "undetected_mean",
    "undetected_lower",
    "undetected_upper",
    "Fraction of the disclosed key",
    "Probability of undetected eavesdropping",
    UNDETECTED_LINIT_LABELS,
    f"{SAVE_PATH}/undetected_L_init_.png",
)

print("Plots generated successfully.")
