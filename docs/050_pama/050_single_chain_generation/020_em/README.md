# Energy minimization

## Provenance

    cp ../000_polyply/default.gro .
    cp ../000_polyply/system.top .
    cp ../000_polyply/custom-ffnonbonded.itp .
    cp ../000_polyply/molecule_with_pairs.itp molecule.itp
    cp -r ../000_polyply/oplsaa.ff .

## Run

    gmx_mpi grompp -f em.mdp -c default.gro -p system.top -o em.tpr -maxwarn 1

    export OMP_NUM_THREADS=1

    nohup mpirun -n 8 gmx_mpi mdrun -deffnm em > gmx.log 2>&1 &
