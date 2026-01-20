# Conversion from GROMACS to LAMMPS

## Provenance

    cp ../030_nvt/custom-ffnonbonded.itp .
    cp ../030_nvt/nvt.gro default.gro
    cp ../030_nvt/molecule.itp .
    cp ../030_nvt/system.top .

## Environment

Created intermol venv with:

    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.10 python3.10-venv python3.10-dev

    python3.10 -m venv ~/venv/intermol
    source ~/venv/intermol/bin/activate
    pip install --upgrade pip

    cd ~/git
    git clone https://github.com/shirtsgroup/InterMol.git
    cd InterMol
    pip install -e .

    pip install numpy
    pip install parmed
    pip install six

## Convert

Converted with and evaluate enrgies with

    intermol-convert --gro_in default.gro system.top --lammps --oname converted --energy --lmppath $(which lmp) --gropath $GMXBIN --verbose

## Output

The difference in potential energy between GROMACS and LAMMPS system should be small, e.g.

```
Energy group summary
=======================================================================
                type     input(gromacs)   output (lammps)     diff (lammps)
-----------------------------------------------------------------------
Not comparable energies: are likely not to be the same
-----------------------------------------------------------------------
        coulomb (LR)      1109.16564941        0.00000000    -1109.16564941
        coulomb (SR)    -27446.34765625        0.00000000    27446.34765625
       coulomb total     -8418.95153809    32838.19554640    41257.14708449
          coulomb-14     17918.23046875        0.00000000   -17918.23046875
            improper      2864.15893555        0.00000000    -2864.15893555
              proper     15565.72070312    18429.91541200     2864.19470887
            vdw (LR)      -238.49467468     -238.63159488       -0.13692020
            vdw (SR)     -3497.00097656        0.00000000     3497.00097656
           vdw total      2523.95649719     2285.21101136     -238.74548583
              vdw-14      6259.45214844        0.00000000    -6259.45214844
-----------------------------------------------------------------------
Comparable energy terms: these should be very close
-----------------------------------------------------------------------
               angle     17501.51953125    17501.51970240        0.00017115
                bond      5284.57617188     5284.58279040        0.00661852
              bonded     41215.97534180    41216.01790480        0.04256300
            dihedral     18429.87963867    18429.91541200        0.03577333
           nonbonded     -5894.99504089    -5892.87865120        2.11638969
           potential     35320.98046875    35323.13967200        2.15920325

---------------- Total Potential Energy Comparison --------------------
Input gromacs potential energy:         35320.98046875
Difference in potential energy from gromacs=>lammps conversion:         2.15920325
=======================================================================
```