using QuantumSavory
using GLMakie
using Random
using DataFrames
using CSV
using Statistics

include("BB84_Protocol.jl")
include("BB84_Utils.jl")

# ----- DEFINING PARAMETERS RANGES -----
# GLOBAL PARAMETERS
seed =                                  Ref(1000)               # initial seed
L_init =                                300                     # total exchanged bits
do_mismatch_experiments =               false
do_undetected_experiments =             false
do_false_positives =                    false
do_key_length_mismatch_experiments =    false
do_key_length_undetected_experiments =  false

# MISMATCH RATIO EXPERIMENT
p_r_mr =                                0.0:0.1:1.0             # probability of error in the quantum channel
repetition_r_mr =                       1:1:1000                # how many times an experiment must be carried out

# PROBABILITY OF UNDETECTED EAVESDROPPING EXPERIMENT
p_pu =                                  0.20                    # probability of error in the quantum channel
k_r_pu =                                0.1:0.1:1.0             # fraction of the disclosed key for eavesdropping detection
repetition_r_pu =                       1:1:10000               # how many times an experiment must be carried out

# EFFECTS OF KEY LENGTH VARIATIONS EXPERIMENT
L_init_r_lv =                           [700, 1000]   # what L_init values should be used [100, 300, 700, 1000]


# create folders if not existent
import Base.Filesystem: mkpath
mkpath("results")
mkpath("results/mismatch_ratio_experiments")
mkpath("results/undetected_eavesdropping_experiments")
mkpath("results/L_init_experiments")

println("STARTING EXPERIMENTS...")

# ----- MISMATCH RATIO EXPERIMENTS -----
if do_mismatch_experiments
    # ideal channel conditions
    df = mismatch_ratio_experiment(false, false, false, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_ideal.csv", df; delim=';')
    println("ratio ideal done")

    # no eavesdropping, bit flip channel
    df = mismatch_ratio_experiment(false, true, false, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_bitflip.csv", df; delim=';')
    println("ratio no eavesdropping, bit flip done")

    # no eavesdropping, phase flip channel
    df = mismatch_ratio_experiment(false, false, true, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_phaseflip.csv", df; delim=';')
    println("ratio no eavesdropping, phase flip done")

    # no eavesdropping, bit and phase flip channel
    df = mismatch_ratio_experiment(false, true, true, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_bitphaseflip.csv", df; delim=';')
    println("ratio no eavesdropping, bit phase flip done")

    # eavesdropping, no bit and phase flip channel
    df = mismatch_ratio_experiment(true, false, false, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping.csv", df; delim=';')
    println("ratio eavesdropping done")

    # eavesdropping, bit flip channel
    df = mismatch_ratio_experiment(true, true, false, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping_bitflip.csv", df; delim=';')
    println("ratio eavesdropping, bit flip done")

    # eavesdropping, phase flip channel
    df = mismatch_ratio_experiment(true, false, true, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping_phaseflip.csv", df; delim=';')
    println("ratio eavesdropping, phase flip done")

    # eavesdropping, bit and phase flip channel
    df = mismatch_ratio_experiment(true, true, true, seed, L_init, p_r_mr, repetition_r_mr)
    CSV.write("results/mismatch_ratio_experiments/mismatch_ratios_eavesdropping_bitphaseflip.csv", df; delim=';')
    println("ratio eavesdropping, bit phase flip done")
end

# ----- UNDETECTED EAVESDROPPING EXPERIMENTS -----
if do_undetected_experiments
    # ideal channel conditions
    df = probability_undetected_experiment(true, false, false, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_undetected_ideal.csv", df; delim=';')
    println("P_und ideal done")

    # bit flip channel
    df = probability_undetected_experiment(true, true, false, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_undetected_bitflip.csv", df; delim=';')
    println("P_und bit flip done")

    # phase flip channel
    df = probability_undetected_experiment(true, false, true, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_undetected_phaseflip.csv", df; delim=';')
    println("P_und phase flip done")

    # bit and phase flip channel
    df = probability_undetected_experiment(true, true, true, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_undetected_bitphaseflip.csv", df; delim=';')
    println("P_und bit phase flip done")
end

# check how frequently false positives occur (relative to the eavesdropping detection)
if do_false_positives
    df = probability_undetected_experiment(false, false, false, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_falsepositive_ideal.csv", df; delim=';')
    df = probability_undetected_experiment(false, true, false, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_falsepositive_bitflip.csv", df; delim=';')
    df = probability_undetected_experiment(false, false, true, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_falsepositive_phaseflip.csv", df; delim=';')
    df = probability_undetected_experiment(false, true, true, seed, L_init, p_pu, k_r_pu, repetition_r_pu)
    CSV.write("results/undetected_eavesdropping_experiments/probability_falsepositive_bitphaseflip.csv", df; delim=';')
end


# ----- EFFECTS OF L_init VARIATION -----
for (L_init_lv) in L_init_r_lv
    println("STARTING L_init VARIATION EXPERIMENTS. L_init: ", L_init_lv)
    if do_key_length_mismatch_experiments
        # MISMATCH RATIO EXPERIMENTS
        # ideal channel conditions
        df = mismatch_ratio_experiment(false, false, false, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_ideal_$(L_init_lv).csv", df; delim=';')
        println("ratio ideal done")

        # no eavesdropping, bit flip channel
        df = mismatch_ratio_experiment(false, true, false, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_bitflip_$(L_init_lv).csv", df; delim=';')
        println("ratio no eavesdropping, bit flip done")

        # no eavesdropping, phase flip channel
        df = mismatch_ratio_experiment(false, false, true, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_phaseflip_$(L_init_lv).csv", df; delim=';')
        println("ratio no eavesdropping, phase flip done")

        # no eavesdropping, bit and phase flip channel
        df = mismatch_ratio_experiment(false, true, true, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_bitphaseflip_$(L_init_lv).csv", df; delim=';')
        println("ratio no eavesdropping, bit phase flip done")

        # eavesdropping, no bit and phase flip channel
        df = mismatch_ratio_experiment(true, false, false, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_eavesdropping_$(L_init_lv).csv", df; delim=';')
        println("ratio eavesdropping done")

        # eavesdropping, bit flip channel
        df = mismatch_ratio_experiment(true, true, false, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_eavesdropping_bitflip_$(L_init_lv).csv", df; delim=';')
        println("ratio eavesdropping, bit flip done")

        # eavesdropping, phase flip channel
        df = mismatch_ratio_experiment(true, true, false, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_eavesdropping_phaseflip_$(L_init_lv).csv", df; delim=';')
        println("ratio eavesdropping, phase flip done")

        # eavesdropping, bit and phase flip channel
        df = mismatch_ratio_experiment(true, true, true, seed, L_init_lv, p_r_mr, repetition_r_mr)
        CSV.write("results/L_init_experiments/mismatch_ratios_eavesdropping_bitphaseflip_$(L_init_lv).csv", df; delim=';')
        println("ratio eavesdropping, bit phase flip done")
    end

    if do_key_length_undetected_experiments
        # UNDETECTED EAVESDROPPING EXPERIMENTS
        # ideal channel conditions
        df = probability_undetected_experiment(true, false, false, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        CSV.write("results/L_init_experiments/probability_undetected_ideal_$(L_init_lv).csv", df; delim=';')
        println("P_und ideal done")

        # bit flip channel
        df = probability_undetected_experiment(true, true, false, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        CSV.write("results/L_init_experiments/probability_undetected_bitflip_$(L_init_lv).csv", df; delim=';')
        println("P_und bit flip done")

        # phase flip channel
        df = probability_undetected_experiment(true, false, true, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        CSV.write("results/L_init_experiments/probability_undetected_phaseflip_$(L_init_lv).csv", df; delim=';')
        println("P_und phase flip done")

        # bit and phase flip channel
        df = probability_undetected_experiment(true, true, true, seed, L_init_lv, p_pu, k_r_pu, repetition_r_pu)
        CSV.write("results/L_init_experiments/probability_undetected_bitphaseflip_$(L_init_lv).csv", df; delim=';')
        println("P_und bit phase flip done")
    end
end

# resume from L_init = 700