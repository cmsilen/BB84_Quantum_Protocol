using QuantumSavory
using QuantumSavory.ProtocolZoo
using Graphs
using ConcurrentSim
using Logging

using GLMakie

global_logger(ConsoleLogger(stderr, Logging.Debug))

# create a register net with 4 registers and 2 slots per register
regs = [Register(2) for _ in 1:4]
net = RegisterNet(regs)

sim = get_time_tracker(net)

# Install EntanglementTracker on every register
for (i, reg) in enumerate(regs)
    ent_tracker = EntanglementTracker(sim, net, i)
    @process ent_tracker()
end

# Install EntanglerProt on all edges
for edge in edges(net)
    ent_prot = EntanglerProt(sim, net, edge.src, edge.dst, rate=1.0)
    @process ent_prot()
end


## Install swappers on intermediate registers
#for i in 2:3
#    swap_prot = SwapperProt(sim, net, i, nodeL= <(i), nodeH= >(i), retry_lock_time=nothing)
#    @process swap_prot()
#end

# Install swappers on intermediate registers
swap_prot_2 = SwapperProt(sim, net, 2, nodeL= <(2), nodeH= >(2), retry_lock_time=nothing)
@process swap_prot_2()
swap_prot_3 = SwapperProt(sim, net, 3, nodeL= <(3), nodeH= >(3), retry_lock_time=nothing, rounds=1)
@process swap_prot_3()

run(sim, 1)

GLMakie.activate!()

# create the plot
fig = Figure(size=(800,400))
_, ax, plt, obs = registernetplot_axis(fig[1,1],net)
display(fig)