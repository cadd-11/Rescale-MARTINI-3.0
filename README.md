# Rescale-MARTINI-3.0

Rescale the interaction strength between beads in MARTINI 3.0 force field for disordered proteins.

Here, the two python scripts are provided to rescale the L-J potential in MARTINI 3.0 force field. 

One script named *PW2_rescaling_martini3.py* which was modified based on the script in this [paper](https://doi.org/10.1021/acs.jctc.1c01042). The improvement is that you are able to rescale factor for epsilon in L-J potential between all bead types and water.

The other script named *TD_modify_epsilon.py* which can rescale epsilon by a function of temperature.
