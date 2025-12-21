function mismatch_ratio_experiment(eavesdropping_event, bit_flip_event, phase_flip_event, seed, L_init, p_r, repetition_r)
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
    for (p, repetition) in Iterators.product(p_r, repetition_r)
        global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p, 0, seed[])
        push!(df, (p = p,
                    repetition = repetition,
                    seed = seed[],
                    global_R_miss = global_R_miss,
                    Z_R_miss = Z_R_miss,
                    X_R_miss = X_R_miss))

        seed[] += 1
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

function probability_undetected_experiment(eavesdropping_event, bit_flip_event, phase_flip_event, seed, L_init, p, k_r, repetition_r)
    # data frame for keeping intermediate results
    df = DataFrame(
        p = Float32[],
        k = Float32[],
        repetition = Int[],
        seed = Int[],
        undetected = Int[]
    )

    # starting experiments, error probability fixed
    for (k, repetition) in Iterators.product(k_r, repetition_r)
        global_R_miss, Z_R_miss, X_R_miss, eve_detected = simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p_pu, k, seed[])
        push!(df, (p = p,
                    k = k,
                    repetition = repetition,
                    seed = seed[],
                    undetected = Int(!eve_detected)))

        seed[] += 1
    end

    # probability by averaging the 0s and 1s in detected column
    df_mean = combine(
        groupby(df, [:k]),
        :undetected => mean => :P_undetect
    )
    return df_mean
end