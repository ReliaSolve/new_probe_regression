# new_probe_regression

Tests the CCTBX/Python version of Probe against the original C++ version.

The current test writes both sets of output and also dumps the atom
information.  It then runs a comparison on the two sets of atom information
and stores it in a .compare file in the outputs directory for each of
the fragments it is testing.

The .compare file reports differences in radius, acceptor/donor/metallic
status, and position (if above a threshold) between atoms in the two models.
It also reports atoms that are only present in one of the models.

## Running

First source init.sh to set up the environment (or set it up manually).

Then run compare.sh to check out versions and compare all fragments.

## Note on compatibility

This code got identical results for 1bt1 and 1xso, and the same scores
for 5fa2 (with a single difference in the potential surface dot count).
The generated surfaces matched for these three cases as well.  The others
had explainable differences where Probe2 was found to be suprior.

These tests passed with Probe2 version 1.0.0.  Later versions of Probe2
will have breaking changes; the first one being to change the Phantom
Hydrogen radii and bond distances to match more recent numbers (they
were both 1.0 in Probe).

