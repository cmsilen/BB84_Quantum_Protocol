import random
from time import sleep

import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.quantum_info import Kraus
from qiskit_aer import AerSimulator
from qiskit_aer.noise import pauli_error, NoiseModel


def simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p, k, seed_gen, verbose=False):
    # initializing the random bit generator, qiskit random bit generator is initialized for each simulation
    random.seed(seed_gen)
    np.random.seed(seed_gen)

    # alice's data structures
    alice_bits = [random.randint(0, 1) for _ in range(L_init)]
    alice_basis = [np.random.choice(["Z", "X"]) for _ in range(L_init)]
    alice_basis = [str(x) for x in alice_basis]
    alice_quantum_key = []

    # eve's data structures
    eve_bits = []
    eve_basis = [np.random.choice(["Z", "X"]) for _ in range(L_init)]
    eve_basis = [str(x) for x in eve_basis]

    # bob's data structures
    bob_bits = []
    bob_basis = [np.random.choice(["Z", "X"]) for _ in range(L_init)]
    bob_basis = [str(x) for x in bob_basis]
    bob_quantum_key = []

    # the quantum channel will be represented by a noise model (it will become a gate)
    # that will apply A with probability p and I with probability (1 - p),
    # with A that depends on the scenario:
    # A = X     bit flip channel
    # A = Z     phase flip channel
    # A = Y     bit-phase flip channel
    operator = "I"
    if bit_flip_event and phase_flip_event:
        operator = "Y"
    elif bit_flip_event:
        operator = "X"
    elif phase_flip_event:
        operator = "Z"
    channel_error = pauli_error([
        (operator, p),
        ("I", 1 - p)
    ])
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(channel_error, ['id'])

    # starting simulations for each bit to send
    for i in range(L_init):
        # quantum channel where Alice sends the qubit, if there is eavesdropping it will be connected to Eve,
        # otherwise it will be connected to Bob
        channel = QuantumRegister(1, "channel")

        # channel that connects Eve to Bob, used only for the eavesdropping event. In this channel Eve will
        # reinitialize the measured qubit to send it to Bob
        eavesdropper_channel = QuantumRegister(1, "eavesdropper_channel")

        # holding the measurements results
        eve_measurement = ClassicalRegister(1, "eve_measurement")
        bob_measurement = ClassicalRegister(1, "bob_measurement")

        # initializing the simulator and quantum circuit
        sim = None
        if eavesdropping_event:
            sim = AerSimulator(noise_model=noise_model, seed_simulator=seed_gen)
        else:
            sim = AerSimulator(seed_simulator=seed_gen)
        channel_circuit = QuantumCircuit(channel, eavesdropper_channel, eve_measurement, bob_measurement)

        # resetting initial states to |0⟩
        channel_circuit.reset(channel[0])
        channel_circuit.reset(eavesdropper_channel[0])

        # alice prepares the qubit, if the bit to send is 1, apply the X gate to get |1⟩,
        # if the chosen basis is X, convert the state using the H gate
        if alice_bits[i] == 1:
            channel_circuit.x(channel[0])
        if alice_basis[i] == "X":
            channel_circuit.h(channel[0])
        channel_circuit.barrier(channel[0])

        # eve intercepts the qubit and measures it, if the chosen basis is X, then a H gate is
        # applied to perform the X basis measurement
        # (procedure to follow if we want to measure in a different basis using a computational basis measurement device).
        # After measurement, Eve will reinitialize the qubit in the other channel (initially at |0⟩) by using a controlled X gate,
        # controlled by the classical bit that contains the measurement result (eventually converted by a H gate)
        if eavesdropping_event:
            if eve_basis[i] == "X":
                channel_circuit.h(channel[0])
            channel_circuit.measure(channel[0], eve_measurement[0])
            # resend qubit
            with channel_circuit.if_test((eve_measurement[0], 1)):
                channel_circuit.x(eavesdropper_channel[0])
            if eve_basis[i] == "X":
                channel_circuit.h(eavesdropper_channel[0])

        # applying noise to the currently active channel by applying the id gate
        if bit_flip_event or phase_flip_event:
            if eavesdropping_event and (bit_flip_event or phase_flip_event):
                channel_circuit.id(eavesdropper_channel[0])
            elif bit_flip_event or phase_flip_event:
                channel_circuit.id(channel[0])

        # bob's measurement
        if eavesdropping_event:
            if bob_basis[i] == "X":
                channel_circuit.h(eavesdropper_channel[0])
            channel_circuit.measure(eavesdropper_channel[0], bob_measurement[0])
        else:
            if bob_basis[i] == "X":
                channel_circuit.h(channel[0])
            channel_circuit.measure(channel[0], bob_measurement[0])

        if i == 0:
            channel_circuit.draw(output='mpl', filename='circuito_bb84.png')
        result = sim.run(channel_circuit, shots=1).result()

        # extracting measurement outcomes
        counts = result.get_counts(channel_circuit)
        measured_bitstring = list(counts.keys())[0]
        if eavesdropping_event:
            eve_outcome = int(measured_bitstring[2])
            bob_outcome = int(measured_bitstring[0])
            eve_bits.append(eve_outcome)
            bob_bits.append(bob_outcome)
        else:
            bob_outcome = int(measured_bitstring[0])
            bob_bits.append(bob_outcome)

        seed_gen + 1

    if verbose:
        print("Alice's bits:\t", alice_bits)
        print("Alice's basis:\t", alice_basis)
        print("Bob's bits:\t", bob_bits)
        print("Bob's basis:\t", bob_basis)
        print("Eve's bits:\t", eve_bits)
        print("Eve's basis:\t", eve_basis)

    # QUANTUM KEY DERIVATION
    for i in range(L_init):
        if alice_basis[i] == bob_basis[i]:
            alice_quantum_key.append(alice_bits[i])
            bob_quantum_key.append(bob_bits[i])
    if verbose:
        print("Alice's quantum key:\t", alice_quantum_key)
        print("Bob's quantum key:\t", bob_quantum_key)
        print("Key length:\t", len(alice_quantum_key))

    # PARTIAL QUANTUM KEY DISCLOSURE FOR EAVESDROPPING DETECTION
    n_disclosed_bits = int(len(alice_quantum_key) * k)
    n_mismatched_key_bits = 0
    for i in range(n_disclosed_bits):
        if alice_quantum_key[i] != bob_quantum_key[i]:
            n_mismatched_key_bits += 1
    if verbose:
        print("mismatched disclosed key bits:\t", n_mismatched_key_bits)

    # COMPUTATIONS OF RATIOS
    # counting mismatches
    global_mismatch_count = 0
    z_mismatch_count = 0
    z_total_count = 0
    x_mismatch_count = 0
    x_total_count = 0
    for i in range(L_init):
        if alice_basis[i] == "Z":
            z_total_count += 1
        elif alice_basis[i] == "X":
            x_total_count += 1

        if alice_bits[i] != bob_bits[i]:
            global_mismatch_count += 1
            if alice_basis[i] == "Z":
                z_mismatch_count += 1
            elif alice_basis[i] == "X":
                x_mismatch_count += 1

    global_mismatch_ratio = global_mismatch_count / L_init
    z_mismatch_ratio = z_mismatch_count / z_total_count
    x_mismatch_ratio = x_mismatch_count / x_total_count

    if verbose:
        print("Global mismatch ratio:\t", global_mismatch_ratio)
        print("Z mismatch ratio:\t", z_mismatch_ratio)
        print("X mismatch ratio:\t", x_mismatch_ratio)
        print("Mismatched bits:\t", global_mismatch_count)

    # EAVESDROPPING DETECTION
    # computing threshold
    threshold = 0
    eve_detected = False
    if (not bit_flip_event and phase_flip_event) or (bit_flip_event and not phase_flip_event):
        threshold = int(len(alice_quantum_key) * (p / 2))
    elif bit_flip_event and phase_flip_event:
        threshold = int(len(alice_quantum_key) * p)
    if n_mismatched_key_bits > threshold:
        eve_detected = True

    if verbose:
        print("Eve detected:\t", eve_detected)

    return global_mismatch_ratio, z_mismatch_ratio, x_mismatch_ratio, eve_detected

res = simulate_bb84(300, True, False, False, 1, 1, 1, True)
print(res)