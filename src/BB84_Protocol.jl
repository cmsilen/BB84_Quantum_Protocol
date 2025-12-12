using QuantumSavory
using GLMakie

# paramaters
num_bits_total = 300
eavesdropping_event = false
bit_flip_event = true
phase_flip_event = false
p = 0.1
seed_gen = 10

reg = Register(1) # We only need one qubit at a time
alice_bases = rand(0:1, num_bits_total) # Alice's random bases. 0 = Z-basis, 1 = X-basis
alice_bits = rand(0:1, num_bits_total)  # Alice's random bits
bob_bases = rand(0:1, num_bits_total)   # Bob's random bases
bob_bits = []
eves_bases = rand(0:1, num_bits_total) # Eve's random bases
eves_bits = []

for i in 1:num_bits_total
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

# seperation of the quantum key by extracting only the matching results
quantum_key = Int[]
num_z_corr = 0
num_x_corr = 0
for i in 1:num_bits_total
    if alice_bases[i] == bob_bases[i]
        if alice_bases[i] == 1
            num_z_corr = num_z_corr + 1
        else
            num_x_corr = num_x_corr + 1
        end

        push!(quantum_key, alice_bits[i])
    end
end

println("Sifted key length: ", length(quantum_key))
println("Sifted key: ", quantum_key)



# mismatch ratio
key_length = length(quantum_key)
global_R_miss = length(quantum_key)/length(alice_bits)

num_Z_basis = count(==(0), alice_bases)
num_X_basis = length(alice_bases)-num_Z_basis
x_R_miss = num_x_corr/key_length
z_R_miss = num_z_corr/key_length



# eavesdropping detection propability
p_und(k) = 1-(3/4)^k
ks = 0:0.1:20               # define the range of k
fs = p_und.(ks)             # calc function values

# printFigure
fig = Figure(size=(800,400))
ax = Axis(fig[1, 1], xlabel="k", ylabel="f(k)", title="f(k) = 1 - (3/4)^k")

# Plot zeichnen
lines!(ax, ks, fs, color=:blue, linewidth=2)

# Figure anzeigen
fig