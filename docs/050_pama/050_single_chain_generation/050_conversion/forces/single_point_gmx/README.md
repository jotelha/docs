# Single point GROMACS force evaluation

## Provenance

    cp ../../custom-ffnonbonded.itp .
    cp ../../default.gro .
    cp ../../system.top .
    cp ../../molecule.itp .

## Run

    gmx grompp -f singlepoint.mdp -c default.gro -p system.top -o singlepoint.tpr

    gmx mdrun -s singlepoint.tpr -deffnm singlepoint

    bash extract_forces.sh  # select system (0)
