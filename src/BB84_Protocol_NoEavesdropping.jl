using QuantumSavory
using GLMakie

num_bits_total = 300
alice_bases = rand(0:1, num_bits_total) # Alice's random bases. 0 = Z-basis, 1 = X-basis
alice_bits = rand(0:1, num_bits_total)  # Alice's random bits
bob_bases = rand(0:1, num_bits_total)   # Bob's random bases
bob_bits = []


for i in 1:num_bits_total
    reg = Register(1)            # only need one qubit at a time

    # preparation of the state
    initialize!(reg[1], Z₁)      # Create a qubit in state |0⟩

    if alice_bits[i] == 1
        apply!(reg[1], X)        # preparation of qubit in state |1>
    end

    # Alice encodes
    # if alice_bases[i]==0 -> in Z basis -> reg state = encoded state : for reg=|0> for |0>, for reg|1> for |1>

    if alice_bases[i] == 1
        apply!(reg[1], H)     # switch to Hadamad basis: |+> for reg=|0> and |-> for reg=|1>
    end

    # Bob measures the qubit
    if bob_bases[i] == 0
        # Z-basis measurement (Computational basis)
        meas_result = project_traceout!(reg, 1, [Z₁, Z₂])-1
    else
        # X-basis measurement (Hadamard basis)
        meas_result = project_traceout!(reg, 1, [X₁, X₂])-1
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
        if alice_bases[i]== 1
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
ks = 0:0.1:20           # define the range of k
fs = p_und.(ks)             # calc function values

# printFigure
fig = Figure(size=(800,400))
ax = Axis(fig[1, 1], xlabel="k", ylabel="f(k)", title="f(k) = 1 - (3/4)^k")

# Plot zeichnen
lines!(ax, ks, fs, color=:blue, linewidth=2)

# Figure anzeigen
display(fig)
