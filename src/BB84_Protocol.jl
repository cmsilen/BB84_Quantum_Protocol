using QuantumSavory
using GLMakie
using Random

# ----- PARAMETERS -----
L_init =                    300     # total exchanged bits
eavesdropping_event =       false   # if there is eavesdropping in the quantum channel
bit_flip_event =            false   # if bit flip events happen
phase_flip_event =          false   # if phase flip events happen
p =                         0.1     # probability of error in the quantum channel
k =                         0.1     # fraction of the disclosed key for eavesdropping detection
bits_mismatch_tolerance =   0.1     # fraction of mismatched key's bits that we are willing to accept before concluding that there ws eavesdropping
seed_gen =                  10      # seed for the random generator

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
        if alice_bits[i] == 0
            current_qubit = Z₁  #|0⟩
        else
            current_qubit = Z₂  #|1⟩
        end
    else
        # X-basis
        if alice_bits[i] == 0
            current_qubit = X₁ # |+⟩
        else
            current_qubit = X₂ # |−⟩
        end
    end

    rho = SProjector(current_qubit)
    if bit_flip_event & phase_flip_event
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

    if eavesdropping_event
        # simulate eavesdropping event
        if eves_bases[i] == 0
            eves_result = project_traceout!(reg, 1, [Z₁, Z₂]) - 1   # -1 to convert from 1/2 to 0/1
            initialize!(reg[1], eves_result == 0 ? Z₁ : Z₂)         # depending on the outcome the qubit gets initialized
        else
            eves_result = project_traceout!(reg, 1, [X₁, X₂]) - 1
            initialize!(reg[1], eves_result == 0 ? X₁ : X₂)
        end
        push!(eves_bits, eves_result)
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
        if alice_bits[i] != bob_bits[i]
            # print for logging purposes
            println("different key bit at index ", i)
        end
    end
end
println("Sifted key length: ", length(alice_quantum_key))



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
println("global mismatch ratio: ", global_R_miss)

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
println("Z mismatch ratio: ", Z_R_miss)
println("X mismatch ratio: ", X_R_miss)


# eavesdropping detection probability
#p_und(k) = 1-(3/4)^k
#ks = 0:0.1:20               # define the range of k
#fs = p_und.(ks)             # calc function values

# printFigure
#fig = Figure(size=(800,400))
#ax = Axis(fig[1, 1], xlabel="k", ylabel="f(k)", title="f(k) = 1 - (3/4)^k")

# Plot zeichnen
#lines!(ax, ks, fs, color=:blue, linewidth=2)

# Figure anzeigen
#fig