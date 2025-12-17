using QuantumSavory
using GLMakie
using Random
using DataFrames
using CSV
using Statistics

include("BB84_Protocol.jl")

# ----- DEFINING PARAMETERS RANGES -----
# GLOBAL PARAMETERS
seed =                          0               # initial seed
L_init =                        300             # total exchanged bits
do_mismatch_experiments =       true
do_undetected_experiments =     false

# MISMATCH RATIO EXPERIMENT
p_r_mr =                        0.0:0.1:1.0     # probability of error in the quantum channel
repetition_r_mr =               1:1:1000        # how many times an experiment must be carried out

# PROBABILITY OF UNDETECTED EAVESDROPPING EXPERIMENT
p_pu =                          0.1             # probability of error in the quantum channel
k_r_pu =                        0.05:0.05:1.0   # fraction of the disclosed key for eavesdropping detection
repetition_r_pu =               1:1:1000        # how many times an experiment must be carried out

function mismatch_ratio_experiment(eavesdropping_event, bit_flip_event, phase_flip_event)
    global seed
    global L_init
    global p_r_mr
    global repetition_r_mr

    # data frame for keeping intermediate results
    df = DataFrame(
        p = Float32[],
        repetition = Int[],
        seed = Int[],
        global_R_miss = Float32[],
        Z_R_miss = Float32[],
        X_R_miss = Float32[],
    )

    # starting experiments
    for (p, repetition) in Iterators.product(p_r_mr, repetition_r_mr)
        global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p, 0, seed)
        push!(df, (p = p,
                    repetition = repetition,
                    seed = seed,
                    global_R_miss = global_R_miss,
                    Z_R_miss = Z_R_miss,
                    X_R_miss = X_R_miss))

        seed += 1
    end
    
    # compute the mean value of each experiment
    df_mean = combine(
        groupby(df, :p),
        :global_R_miss => mean => :global_R_miss_mean,
        :Z_R_miss      => mean => :Z_R_miss_mean,
        :X_R_miss      => mean => :X_R_miss_mean,
    )
    return df_mean
end

function probability_undetected_experiment(eavesdropping_event, bit_flip_event, phase_flip_event)
    global seed
    global L_init
    global p_pu
    global k_r_pu
    global repetition_r_pu

    # data frame for keeping intermediate results
    df = DataFrame(
        p = Float32[],
        k = Float32[],
        repetition = Int[],
        seed = Int[],
        detected = Int[]
    )

    # starting experiments, error probability fixed
    for (k, repetition) in Iterators.product(k_r_pu, repetition_r_mr)
        global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p_pu, 0, seed)
        push!(df, (p = p_pu,
                    k = k,
                    repetition = repetition,
                    seed = seed,
                    detected = Int(!eve_detected)))

        seed += 1
        println(eve_detected)
    end

    # probability by averaging the 0s and 1s in detected column
    df_mean = combine(
        groupby(df, [:k]),
        :detected => mean => :P_detect
    )
    return df_mean
end


# create folders if not existent
import Base.Filesystem: mkpath
mkpath("mismatch_ratio_experiments")
mkpath("undetected_eavesdropping_experiments")

# ----- MISMATCH RATIO EXPERIMENTS -----
if do_mismatch_experiments
    # ideal channel conditions
    df = mismatch_ratio_experiment(false, false, false)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_ideal.csv", df; delim=';')

    # no eavesdropping, bit flip channel
    df = mismatch_ratio_experiment(false, true, false)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_bitflip.csv", df; delim=';')

    # no eavesdropping, phase flip channel
    df = mismatch_ratio_experiment(false, false, true)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_phaseflip.csv", df; delim=';')

    # no eavesdropping, bit and phase flip channel
    df = mismatch_ratio_experiment(false, true, true)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_bitphaseflip.csv", df; delim=';')

    # eavesdropping, no bit and phase flip channel
    df = mismatch_ratio_experiment(true, false, false)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_eavesdropping.csv", df; delim=';')

    # eavesdropping, bit flip channel
    df = mismatch_ratio_experiment(true, true, false)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_eavesdropping_bitflip.csv", df; delim=';')

    # eavesdropping, phase flip channel
    df = mismatch_ratio_experiment(true, true, false)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_eavesdropping_phaseflip.csv", df; delim=';')

    # eavesdropping, bit and phase flip channel
    df = mismatch_ratio_experiment(true, true, true)
    CSV.write("mismatch_ratio_experiments/mismatch_ratios_eavesdropping_bitphaseflip.csv", df; delim=';')
end

# ----- UNDETECTED EAVESDROPPING EXPERIMENTS -----
if do_undetected_experiments
    # ideal channel conditions
    df = probability_undetected_experiment(true, false, false)
    CSV.write("undetected_eavesdropping_experiments/probability_undetected_ideal.csv", df; delim=';')

    # bit flip channel
    df = probability_undetected_experiment(true, true, false)
    CSV.write("undetected_eavesdropping_experiments/probability_undetected_bitflip.csv", df; delim=';')

    # phase flip channel
    df = probability_undetected_experiment(true, false, true)
    CSV.write("undetected_eavesdropping_experiments/probability_undetected_phaseflip.csv", df; delim=';')

    # bit and phase flip channel
    df = probability_undetected_experiment(true, true, true)
    CSV.write("undetected_eavesdropping_experiments/probability_undetected_bitphaseflip.csv", df; delim=';')
end