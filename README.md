# Amas-FF14-Combat-Sim_source
Open source code for Ama's FF14 Combat Sim.

# Quick start
If you would like to run the sim but do not want to install it, go to the [Python Notebook Github](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim) and follow the instruction to open and use *CoreSimulator.ipynb*.

If you would like to install the sim to run locally, run ```pip install ama-xiv-combat-sim``` on your machine to install the core packages. You may want to refer to some of the code in the [Python Notebook](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim/blob/main/CoreSimulator.ipynb) to grab some visualization/plotting code that visualizes the sim's output.

# About
This open-source package simulates the damage of given gearsets and rotations, producing the full distributions over damage values and various statistics, like the expected max damage over N runs (useful for parsers). Currently, all lvl 100 standard combat classes are supported. For issues/feature requests and news, join the [Discord](https://discord.gg/CV6sHj8h9D) server.

Unlike other simulators/spreadsheets, this gives more than just expected damage with an approximation of damage variance- this is an accurate [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method) simulation that gives the full range and distribution over all possible damage values. This tool is an installable pip package, and is also in a standalone [Python Notebook](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim/blob/main/CoreSimulator.ipynb) that can be run on Google's Colab in 2 mouse clicks.

The sim's main computation engine is written in Numpy, relying on parallelized matrix-based computations for the heavy lifting. It runs fairly fast (a typical ~30s opener with 1M samples takes about 1-2 seconds on a single CPU).

The tool has four advantages over existing simulators/spreadsheets:

1) handles the simulation of all FF14 job classes in a single place- no need to maintain multiple spreadsheets, etc.,

2) incorporates all damage rolls and crit/dh procs on a per-damage-instance basis, and rolls them every time the sim is run,

3) enables the building of several useful community tools that either don't exist, or can be streamlined, using this sim as a backend, and

4) allows for the incorporation of procs in the simulation process itself.

Some examples of useful tools is a *kill time estimator*, that takes a 1) full 8-player rotation including LB usage, and 2) a target boss HP values, and outputs a distribution over expected kill times. To see a demonstration of this and other capabilities built on top of the sim, please refer to the [Python Notebook Github](https://github.com/Amarantine-xiv/Amas-FF14-Combat-Sim).

# Usage

## Imports
After installation, make sure to *import ama-xiv-combat-sim* so that paths, etc. are set up. After this, you can import sub-packages/functions/files as you wish, and use them. Rotations can be specified both in code in the sim itself, and by passing in CSV files.

## Example Single Target, Single Player rotation, typed directly into the sim.
```
import ama_xiv_combat_sim

from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.rotation_import_utils.csv_utils import CSVUtils
from ama_xiv_combat_sim.simulator.skills import create_skill_library, SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder

# Creates the FF14 game skill library
SKILL_LIBRARY = create_skill_library()

# Our stats
stats = Stats(wd=132, weapon_delay=3.36, main_stat=3330, det_stat=2182, crit_stat=2596, dh_stat=940, speed_stat=400, tenacity=601, job_class = 'WAR')

rb = RotationBuilder(stats, SKILL_LIBRARY, ignore_trailing_dots=True, enable_autos=True)

# Specify party status effects first.  In general, this is whatever the name of the button you would press in-game is.
# Note the format is (timestamp, skill name, job class)
rb.add(6.3, 'Chain Stratagem', job_class='SCH')
rb.add(7.1, 'Battle Litany', job_class='DRG')
rb.add(0.8, 'Arcane Circle', job_class='RPR')
rb.add(6.28, 'Embolden', job_class='RDM')
rb.add(6.3, 'Dokumori', job_class='NIN') 

# Actual skill usage for our class, WAR.
# Note here, when uses add_next, we need only specify the name of the skill. In general, this is whatever the name of the button you would press in-game is.
rb.add_next('Tomahawk')
rb.add_next('Infuriate')
rb.add_next('Heavy Swing')
rb.add_next('Maim')
rb.add_next('Grade 8 Tincture')
rb.add_next("Storm's Eye")
rb.add_next('Inner Release')
rb.add_next('Inner Chaos')
rb.add_next('Upheaval')
rb.add_next('Onslaught')
rb.add_next('Primal Rend')
rb.add_next('Inner Chaos')
rb.add_next('Onslaught')
rb.add_next('Fell Cleave')
rb.add_next('Onslaught')
rb.add_next('Fell Cleave')
rb.add_next('Fell Cleave')
rb.add_next('Heavy Swing')
rb.add_next('Maim')
rb.add_next("Storm's Path")
rb.add_next('Fell Cleave')
rb.add_next('Inner Chaos')

# Standard code to build the sim for a rotation and run it
db = DamageBuilder(stats, SKILL_LIBRARY)
sim = DamageSimulator(stats, db.get_damage_instances(rb.get_skill_timing()), num_samples=100000) #for speed, we only use 100k samples.
dps = sim.get_dps() # dps values of our WAR rotation
damage = sim.get_raw_damage() # raw damage of our WAR rotation
per_skill_damage = sim.get_per_skill_damage(rb) # get per-damage-instance information
damage_ranges = sim.get_damage_ranges() # get damage ranges on each skill, detailing crit/dh damage ranges and probabilities.

# Visualization code here. Whatever you want to do to visualize the outputs, etc. Or refer to the Python notebook for examples.
```

## Example Single Target, Single Player rotation, from a CSV file.
```
import ama_xiv_combat_sim
import os

from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.rotation_import_utils.csv_utils import CSVUtils
from ama_xiv_combat_sim.simulator.skills import create_skill_library, SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder

#The name of our rotation file. The expected columns are "Time", "skill_name", "job_class", and "skill_conditional" in that order. See my_rotation.csv in this repo for an example.
csv_filename = 'my_rotation.csv'

# Creates the FF14 game skill library
SKILL_LIBRARY = create_skill_library()

# Our stats
stats = Stats(wd=132, weapon_delay=3.36, main_stat=3330, det_stat=2182, crit_stat=2596, dh_stat=940, speed_stat=400, tenacity=601, job_class = 'WAR')

rb = RotationBuilder(stats, SKILL_LIBRARY, ignore_trailing_dots=True, enable_autos=True)

if not os.path.exists(csv_filename):
  print('File does not exist: {}. Make sure you are in the right directory and have the right file name: '.format(csv_filename))
else:
    rb, _ = CSVUtils.populate_rotation_from_csv(rb, csv_filename)

# Standard code to build the sim for a rotation and run it
db = DamageBuilder(stats, SKILL_LIBRARY)
sim = DamageSimulator(stats, db.get_damage_instances(rb.get_skill_timing()), num_samples=100000) #for speed, we only use 100k samples.
dps = sim.get_dps()
damage = sim.get_raw_damage()
per_skill_damage = sim.get_per_skill_damage(rb) # get per-damage-instance information
damage_ranges = sim.get_damage_ranges() # get damage ranges on each skill, detailing crit/dh damage ranges and probabilities.

```


# Acknowledgements
I'd like to thank the following people/groups for their help! Without them, this sim would not be at all possible:

[The Balance](https://www.thebalanceffxiv.com/)

Io Whitespirit

Hint and [Hint's damage calc repo](https://github.com/hintxiv/reassemble)

Fürst

Apollo Van-waddleburg

IAmPythagoras and [IAmPythagoras's FFXIV-Combat-Simulator](https://github.com/IAmPythagoras/FFXIV-Combat-Simulator) and [Discord](https://discord.com/invite/mZXKUNy2sw)

Cless

Kaiser08259

Mahdi (from the Allagan Studies Discord server)
