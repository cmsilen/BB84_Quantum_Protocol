using QuantumSavory
using GLMakie
using Random
using DataFrames
using CSV

include("BB84_Protocol.jl")

# ----- DEFINING PARAMETERS RANGES -----
L_init =                        300     # total exchanged bits
eavesdropping_event_r =         [false, true]   # if there is eavesdropping in the quantum channel
bit_flip_event_r =              [false, true]   # if bit flip events happen
phase_flip_event_r =            [false, true]   # if phase flip events happen
p_r =                           0.0:0.1:1.0     # probability of error in the quantum channel
k_r =                           0.0:0.1:1.0     # fraction of the disclosed key for eavesdropping detection
bits_mismatch_tolerance_r =     0.0:0.1:1.0     # fraction of mismatched key's bits that we are willing to accept before concluding that there ws eavesdropping
repetition_r =                  1:1:20
seed =                          0               # initial seed

function mismatch_ratio_experiment(eavesdropping_event, bit_flip_event, phase_flip_event)
    global seed
    global p_r
    global repetition_r
    df = DataFrame(
        p = Float32[],
        repetition = Int[],
        seed = Int[],
        global_R_miss = Float32[],
        Z_R_miss = Float32[],
        X_R_miss = Float32[],
    )
    for (p, repetition) in Iterators.product(p_r, repetition_r)
        global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p, 0, 0, seed)
        push!(df, (p = p,
                    repetition = repetition,
                    seed = seed,
                    global_R_miss = global_R_miss,
                    Z_R_miss = Z_R_miss,
                    X_R_miss = X_R_miss))

        seed += 1
    end
    return df
end

function probability_undetected_experiment(eavesdropping_event, bit_flip_event, phase_flip_event)
    # TODO implement
end


# create folders if not existent
import Base.Filesystem: mkpath
mkpath("mismatch_ratio_experiments")
mkpath("undetected_eavesdropping_experiments")

# ----- MISMATCH RATIO EXPERIMENTS -----
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


# ----- UNDETECTED EAVESDROPPING EXPERIMENTS -----
# TODO how should these tests be carried out?
# We should test in how many runs eve is detected as a function of the parameter k in all eavesdropping scenarios,
# but some scenarios contain the channel errors, hence there also is the parameter p, should it also be in function of p?