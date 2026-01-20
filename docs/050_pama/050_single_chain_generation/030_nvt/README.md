Provenance:
# NVT equilibration

## Provenance

    cp ../020_em/custom-ffnonbonded.itp .
    cp ../020_em/em.gro default.gro
    cp ../020_em/molecule.itp .
    cp ../020_em/system.top .
    cp -r ../020_em/oplsaa.ff .

## Run

    gmx_mpi grompp -f nvt.mdp -c default.gro -p system.top -o nvt.tpr -maxwarn 2

    nohup mpirun -n 4 gmx_mpi mdrun -deffnm nvt > gmx.log 2>&1 &
