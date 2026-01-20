# Per-atom force comparison

First, run single-point force evaluations with GROMACS and LAMMPS in sub folders.

Next, compare forces with

    $ bash compare_forces.sh 
    Max ΔF: 0.819140 atom 370

Inspect the generated file

    $ head -n 4 force_compare.dat 
    1 1601.764687 1601.617599 0.258313
    2 660.259376 660.248646 0.077172
    3 827.363973 827.391221 0.069105
    4 926.493817 926.579402 0.087651

Columns are atom ID, gmx force vector magnitude, lmp force vector magnitude, gmx - lmp force vector diff magnitude.

The forces should agree closely for each atom.
