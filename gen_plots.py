import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# Configurazione
# =========================
CSV_PATH_MISMATCH = "results/mismatch_ratio_experiments"
CSV_PATH_UNDETECTED = "results/undetected_eavesdropping_experiments"
SAVE_PATH = "plots"
os.makedirs(SAVE_PATH, exist_ok=True)

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

ALPHA = 0.25                  # trasparenza banda

df_array_mismatch_noeavesdropping = []
for csv in CSVS_MISMATCH_NOEAVESDROPPING:
    df = pd.read_csv(f"{CSV_PATH_MISMATCH}/{csv}", sep=";")
    df_array_mismatch_noeavesdropping.append(df)

df_array_mismatch_eavesdropping = []
for csv in CSVS_MISMATCH_EAVESDROPPING:
    df = pd.read_csv(f"{CSV_PATH_MISMATCH}/{csv}", sep=";")
    df_array_mismatch_eavesdropping.append(df)

df_array_undetected = []
for csv in CSVS_UNDETECTED:
    df = pd.read_csv(f"{CSV_PATH_UNDETECTED}/{csv}", sep=";")
    df_array_undetected.append(df)

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

print("Plots generated successfully.")
