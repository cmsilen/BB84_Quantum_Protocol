using QuantumSavory
using GLMakie
using Random
using DataFrames
using CSV

function initialize_reg(reg, state, bit_flip_event, phase_flip_event, p)
    rho = SProjector(state)
    if bit_flip_event && phase_flip_event
        # both, represented by the operator XZ = Y (I hope)
        rho_after_noise = (1 - p) * rho + p * Y * rho * Y
    elseif bit_flip_event
        # bit flip with probability p
        rho_after_noise = (1 - p) * rho + p * X * rho * X
    elseif phase_flip_event
        # phase flip with probability p
        rho_after_noise = (1 - p) * rho + p * Z * rho * Z
    else
        # no noise, pure state
        rho_after_noise = rho
    end
    initialize!(reg, 1, rho_after_noise)
end

function simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p, k, seed_gen, verbose = false)
    Random.seed!(seed_gen)              # initializing the random bit generator
    reg = Register(1)                   # represents the quantum channel
    alice_bases = rand(0:1, L_init)     # Alice's random bases. 0 = Z-basis, 1 = X-basis
    alice_bits = rand(0:1, L_init)      # Alice's random bits
    alice_quantum_key = Int[]           # Alice's derived key
    bob_bases = rand(0:1, L_init)       # Bob's random bases
    bob_bits = []                       # Bob's measured bits
    bob_quantum_key = Int[]             # Bob's derived key
    eves_bases = rand(0:1, L_init)      # Eve's random bases
    eves_bits = []                      # Eve's measured bits

    for i in 1:L_init
        # Alice prepares the qubit
        if alice_bases[i] == 0
            # Z-basis
            current_qubit = (alice_bits[i] == 0) ? Z₁ : Z₂
        else
            # X-basis
            current_qubit = (alice_bits[i] == 0) ? X₁ : X₂
        end
        if eavesdropping_event
            # initialize without noise
            initialize_reg(reg, current_qubit, false, false, p)
        else
            initialize_reg(reg, current_qubit, bit_flip_event, phase_flip_event, p)
        end

        if eavesdropping_event
            # simulate eavesdropping event
            if eves_bases[i] == 0
                eves_result = project_traceout!(reg, 1, [Z₁, Z₂]) - 1   # -1 to convert from 1/2 to 0/1
                current_qubit = (eves_result == 0) ? Z₁ : Z₂              # depending on the outcome the qubit gets initialized
            else
                eves_result = project_traceout!(reg, 1, [X₁, X₂]) - 1
                current_qubit = (eves_result == 0) ? X₁ : X₂
            end
            push!(eves_bits, eves_result)
            initialize_reg(reg, current_qubit, bit_flip_event, phase_flip_event, p)
        end

        # Bob measures the qubit
        if bob_bases[i] == 0
            # Z-basis measurement
            meas_result = project_traceout!(reg, 1, [Z₁, Z₂]) - 1
        else
            # X-basis measurement
            meas_result = project_traceout!(reg, 1, [X₁, X₂]) - 1
        end

        # Store Bob's measurement result
        push!(bob_bits, meas_result)
    end

    # seperation of the quantum key by extracting only the bits associated to matching bases
    for i in 1:L_init
        if alice_bases[i] == bob_bases[i]
            push!(alice_quantum_key, alice_bits[i])
            push!(bob_quantum_key, bob_bits[i])
            if verbose && alice_bits[i] != bob_bits[i]
                # print for logging purposes
                println("different key bit at index ", i)
            end
        end
    end
    if verbose
        println("Sifted key length: ", length(alice_quantum_key))
    end

    # disclosure of bits for checking if eavesdropping has occurred
    quantum_key_length = length(alice_quantum_key)
    n_disclosed_bits = Int(floor(k * quantum_key_length))
    mismatched_disclosed_bits = 0
    for i in 1:n_disclosed_bits
        if alice_quantum_key[i] != bob_quantum_key[i]
            mismatched_disclosed_bits += 1
        end
    end
    if verbose
        println("mismatched bits found in the disclosed bits: ", mismatched_disclosed_bits)
    end

    # ----- METRICS -----
    # global mismatch ratio
    # ratio of the total number of mismatched bits between Alice's and Bob to L_init
    global_R_miss = 0
    mismatched_bits = 0
    for i in 1:L_init
        if alice_bits[i] != bob_bits[i]
            mismatched_bits += 1
        end
    end
    global_R_miss = mismatched_bits / L_init
    if verbose
        println("global mismatch ratio: ", global_R_miss)
    end

    # Z mismatch ratio, X mismatch ratio
    # 1) ratio of mismatched bits to L_init when states are encoded in the Z basis {|0⟩, |1⟩}
    # 2) ratio of mismatched bits to L_init when states are encoded in the X basis {|+⟩, |-⟩}

    n_Z_base = 0
    n_Z_base_mismatch = 0
    n_X_base = 0
    n_X_base_mismatch = 0
    for i in 1:L_init
        if alice_bases[i] == 0
            n_Z_base += 1
            if alice_bits[i] != bob_bits[i]
                n_Z_base_mismatch += 1
            end
        end
        if alice_bases[i] == 1
            n_X_base += 1
            if alice_bits[i] != bob_bits[i]
                n_X_base_mismatch += 1
            end
        end
    end
    Z_R_miss = n_Z_base_mismatch / n_Z_base
    X_R_miss = n_X_base_mismatch / n_X_base
    if verbose
        println("Z mismatch ratio: ", Z_R_miss)
        println("X mismatch ratio: ", X_R_miss)
    end

    # undetected eavesdropping probability TODO REFINE BECAUSE TOO MUCH FALSE POSITIVES
    # events legend:
    #       E: error on a bit of the key (so  it is already in the same base for both alice and bob)
    #       Z: the common base is Z
    #       X: the common base is X
    #       BF: bit flip has occurred
    #       PF: phase flip has occurred
    #       BPF: both flips have occurred
    #
    # case bit flip:
    #       P{E} = P{E | Z, BF} * P{Z} * P{BF} + P{E | X, BF} * P{X} * P{BF} = 1 * 1/2 * p + 0 * 1/2 * p = p/2
    # case phase flip:
    #       P{E} = P{E | Z, PF} * P{Z} * P{PF} + P{E | X, PF} * P{X} * P{PF} = 0 * 1/2 * p + 1 * 1/2 * p = p/2
    # case both:
    #       P{E} = P{E | Z, BPF} * P{Z} * P{PBPFF} + P{E | X, BPF} * P{X} * P{BPF} = 1 * 1/2 * p + 1 * 1/2 * p = p
    #
    # so on average, given n_disclosed_bits disclosed bits, we expect n_disclosed_bits * P{E} mismatched bits due to channel errors
    eve_detected = false
    threshold = 0
    if (!bit_flip_event && phase_flip_event) || (bit_flip_event && !phase_flip_event)
        threshold = Int(floor(n_disclosed_bits * p / 2))
    elseif bit_flip_event && phase_flip_event
        threshold = Int(floor(n_disclosed_bits * p))
    end
    if verbose
        print(mismatched_disclosed_bits)
        print("/")
        print(n_disclosed_bits)
        print(" ")
        println(threshold)
    end
    if mismatched_disclosed_bits > threshold
        eve_detected = true
    end

    return global_R_miss, Z_R_miss, X_R_miss, eve_detected
end