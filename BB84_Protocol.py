from qiskit import QuantumCircuit
import qiskit.quantum_info as qi
import random
import numpy as np

X = qi.Operator.from_label('X')
Y = qi.Operator.from_label('Y')
Z = qi.Operator.from_label('Z')

Z1 = qi.Statevector.from_label("0")   # |0⟩
Z2 = qi.Statevector.from_label("1")   # |1⟩
X1 = qi.Statevector.from_label("+")   # |+⟩
X2 = qi.Statevector.from_label("-")   # |−⟩

def initialize_state(base, bit, bit_flip_event, phase_flip_event, p):
    if base == 0:
        state = Z1 if bit == 0 else Z2
    else:
        state = X1 if bit == 0 else X2

    rho = qi.DensityMatrix(state)

    if bit_flip_event & phase_flip_event:
        rho_after_noise = (1-p)* rho + p * Y  @  rho  @  Y
    elif bit_flip_event:
        rho_after_noise = (1-p) * rho + p * X  @  rho  @ X
    elif phase_flip_event:
        rho_after_noise = (1-p)* rho + p * Z  @  rho  @ Z
    else:
        rho_after_noise = rho

    return rho_after_noise

def project_traceout(rho, projectors):
    probs = []
    for P in projectors:
        P = qi.DensityMatrix(P).data
        val = np.trace(P @ rho.data @ P)
        probs.append(np.real(val))

    probs = np.array(probs)   # convert into a numerical array
    probs /= probs.sum()      # make sure that propabilities are normed

    result = np.random.choice(len(projectors), p=probs)

    return result


def simulate_bb84(L_init, eavesdropping_event, bit_flip_event, phase_flip_event, p, k, seed_gen, verbose=False):
    random.seed(seed_gen)  # initializing the random bit generator
    np.random.seed(seed_gen)

    alice_bases = [random.randint(0, 1) for _ in range(L_init)]  # Alice's random bases. 0=Z-basis, 1=X-basis
    alice_bit = [random.randint(0, 1) for _ in range(L_init)]  # Alice's random bits
    alice_quantum_key = []  # Alice's derived key

    eves_bases = [random.randint(0, 1) for _ in range(L_init)]  # Eve's random bases
    eves_bit = []  # Eve's measures bits

    bob_bases = [random.randint(0, 1) for _ in range(L_init)]  # Bob's random bases. 0=Z-basis, 1=X-basis
    bob_bit = []  # Bob's measured bits
    bob_quantum_key = []  # Bob's derived key

    for i in range(L_init):
        # alice prepares the qubit
        if eavesdropping_event:
            rho = initialize_state(alice_bases[i], alice_bit[i], False, False, p)
        else:
            rho = initialize_state(alice_bases[i], alice_bit[i], bit_flip_event, phase_flip_event, p)

        if eavesdropping_event:
            # simulate eavesdropping event
            if eves_bases[i] == 0:
                eves_result = project_traceout(rho, [Z1, Z2])
            else:
                eves_result = project_traceout(rho, [X1, X2])

            eves_bit.append(eves_result)
            rho = initialize_state(eves_bases[i], eves_result, bit_flip_event, phase_flip_event, p)

        # bobs measurement
        if bob_bases[i] == 0:
            bob_result = project_traceout(rho, [Z1, Z2])
        else:
            bob_result = project_traceout(rho, [X1, X2])

        bob_bit.append(bob_result)

    assert len(alice_bit) == len(bob_bit)
    # -------- extraction of quantum key --------
    for i in range(L_init):
        if alice_bases[i] == bob_bases[i]:
            alice_quantum_key.append(alice_bit[i])
            bob_quantum_key.append(bob_bit[i])
            # if verbose and alice_bit[i] != bob_bit[i]:
            # print("Different key bit at index", i)

    if verbose:
        print("Sifted key length:", len(alice_quantum_key))

    # -------- Disclosure --------
    n_disclosed = int(np.floor(k * len(alice_quantum_key)))
    mismatched_disclosed = sum(
        1 for i in range(n_disclosed)
        if alice_quantum_key[i] != bob_quantum_key[i]
    )

    # -------- Metrics --------
    global_R_miss = sum(
        1 for i in range(L_init)
        if alice_bit[i] != bob_bit[i]
    ) / L_init

    Z_total = Z_miss = X_total = X_miss = 0

    for i in range(L_init):
        if alice_bases[i] == 0:
            Z_total += 1
            if alice_bit[i] != bob_bit[i]:
                Z_miss += 1
        else:
            X_total += 1
            if alice_bit[i] != bob_bit[i]:
                X_miss += 1

    Z_R_miss = Z_miss / Z_total if Z_total else 0
    X_R_miss = X_miss / X_total if X_total else 0

    # -------- Eve detection --------
    if (bit_flip_event ^ phase_flip_event):
        threshold = int(np.floor(n_disclosed * p / 2))
    elif bit_flip_event and phase_flip_event:
        threshold = int(np.floor(n_disclosed * p))
    else:
        threshold = 0

    eve_detected = mismatched_disclosed > threshold

    if verbose:
        print("Global mismatch:", global_R_miss)
        print("Z mismatch:", Z_R_miss)
        print("X mismatch:", X_R_miss)
        print("Disclosed mismatches:", mismatched_disclosed, "/", n_disclosed)
        print("Threshold:", threshold)

    return global_R_miss, Z_R_miss, X_R_miss, eve_detected

simulate_bb84(300, True, True, True, 0.9, 0.1, 10, True)