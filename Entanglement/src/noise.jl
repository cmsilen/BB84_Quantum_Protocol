# how to model noise

using QuantumSavory

bell_state = (Z₁ ⊗ Z₁ + Z₂ ⊗ Z₂)/ √2
bell_state_dm = SProjector(bell_state)

comp_mixed_state = MixedState(bell_state_dm)

w = 0.95 # depolarizing prop is 1-with
depolarizing = w*bell_state_dm + (1-w)*comp_mixed_state


# dephased(rho) = w * rho + (1-w)*Z*rho*Z
dephased = w*bell_state_dm + (1-w)*(Z⊗I)*bell_state_dm*(Z⊗I)

# t --> E(rho) = e^{-t/T} rho + (1-e^{-t/T}) I/2     with T as a coherent time (tells you how fast a process is) -> t needs to be one order of magnitude lower
background_noise = T1Decay(0.5)

reg = Register(5, [T1Decay(1.0), T2Dephasing(), ])