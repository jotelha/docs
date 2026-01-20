Provenance:
# NVT equilibration

## Provenance

    cp ../020_em/custom-ffnonbonded.itp .
    cp ../020_em/em.gro default.gro
    cp ../020_em/molecule.itp .
    cp ../020_em/system.top .

## Run

    gmx_mpi grompp -f nvt.mdp -c default.gro -p system.top -o nvt.tpr -maxwarn 1

    export OMP_NUM_THREADS=1

    nohup mpirun -n 8 gmx_mpi mdrun -deffnm nvt > gmx.log 2>&1 &
