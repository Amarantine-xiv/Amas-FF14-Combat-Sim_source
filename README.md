# Amas-FF14-Combat-Sim_source
Public source code for Ama's Combat Sim.

# Quick start
If you would like to run the sim but do not want to install it, go to the [Python Notebook Github](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim) and follow the instruction to open and use *CoreSimulator.ipynb*.

If you would like to install the sim to run locally, run *pip install ama-xiv-combat-sim* on your machine to install the core packages. You may want to refer to some of the code in the [Python Notebook][(https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim/blob/main/CoreSimulator.ipynb) to grab some visualization/plotting code that visualizes the sim's output.

# About
This open-source package simulates the damage of given gearsets and rotations, producing the full distributions over damage values and various statistics, like the expected max damage over N runs (useful for parsers). Currently, all lvl 90 standard combat classes are supported (lvl 100 and Dawntrail support will come in the future, after Dawntrail is released). For issues/feature requests and news, join the [Discord](https://discord.gg/CV6sHj8h9D) server.

Unlike other simulators/spreadsheets, this gives more than just expected damage with an approximation of damage variance- this is an accurate [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method) simulation that gives the full range and distribution over all possible damage values. This tool is available here is an installable pip package, and also in a standalone [Python Notebook][(https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim/blob/main/CoreSimulator.ipynb) that can be run on Google's Colab.

The sim's main computation engine is written in Numpy, relying on parallelized matrix-based computations for the heavy lifting. It runs fairly fast (a typical ~30s opener with 1M samples takes about 1-2 seconds on a single CPU).

The tool has four advantages over existing simulators/spreadsheets:

1) handles the simulation of all FF14 job classes in a single place- no need to maintain multiple spreadsheets, etc.,

2) incorporates all damage rolls and crit/dh procs on a per-damage-instance basis, and rolls them every time the sim is run (currently you can do 1M simulation runs in a couple seconds),

3) enables the building of several useful community tools that either don't exist, or can be streamlined, using this sim as a backend (or just a loaded Python notebook as a hack), and

4) allows for the incorporation of procs in the simulation process itself.
