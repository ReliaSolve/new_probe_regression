# new_probe_regression

Tests the CCTBX/Python version of Probe against the original C++ version.

The current test writes both sets of output and also dumps the atom
information.  It then runs a comparison on the two sets of atom information
and stores it in a .compare file in the outputs directory for each of
the fragments it is testing.

The .compare file reports differences in radius, acceptor/donor/metallic
status, and position (if above a threshold) between atoms in the two models.
It also reports atoms that are only present in one of the models.

# Running

First source init.sh to set up the environment (or set it up manually).

Then run compare.sh to check out versions and compare all fragments.

