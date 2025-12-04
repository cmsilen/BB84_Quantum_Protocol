using QuantumSavory
using QuantumSavory.ProtocolZoo

using Logging
global_logger(ConsoleLogger(stderr, Logging.Debug))


# create a register net with 5 registers and 3 slots per register
regs = [Register(3) for _ in 1:5]
net = RegisterNet(regs)

using ConcurrentSim
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

swap_prot_2 = SwapperProt(sim, net, 2, nodeL= <(2), nodeH= >(2), retry_lock_time=nothing)
@process swap_prot_2()

swap_prot_4 = SwapperProt(sim, net, 4, nodeL= <(4), nodeH= >(4), retry_lock_time=nothing)
@process swap_prot_4()

swap_prot_3 = SwapperProt(sim, net, 3, nodeL= <(3), nodeH= >(3), retry_lock_time=nothing)
@process swap_prot_3()

run(sim, 1)

using GLMakie
GLMakie.activate!()

using Graphs
# create the plot
fig = Figure(size=(800,400))
_, ax, plt, obs = registernetplot_axis(fig[1,1],net)
display(fig)