# Polyply

PAMA parameters for various monomer building blocks are found within extended oplsaaLigParGen library of [https://github.com/jotelha/polyply_1.0/tree/2025-12-01-PAMA-parameters].

## Use

First, generate sequence with

    polyply gen_seq -from_string A:1:1:CH3n-1.0 B:58:1:MMA-1.0 C:69:1:LA-0.217,EH-0.493,ST-0.290 -o sequence.json -name PAMA_BLOCK -seq A B C A -connect 0:1:0-0 1:2:57-0 2:3:68-0

Next, generate topology with

    polyply gen_params -lib oplsaaLigParGen -o molecule.itp -name PAMA_BLOCK -seqf sequence.json

Eventually, generate coordinates with

    polyply gen_coords -p system.top -o default.gro -name PAMA_BLOCK -dens 300

Now, polyply does not get the 1-4 pairs right. Generate all 1-4 pairs from topology with

    python generate_pairs_from_dihedrals.py -i molecule.itp -o pairs.dat

and insert them into the ITP file with

    python insert_custom_pairs_list.py -p pairs.dat -i molecule.itp -o molecule_with_pairs.itp

Double-check that charge of generated polymer is zero with

    python check_total_charge.py molecule.itp

Double-check molecular weight with

    $ python check_molecular_weight.py default.gro 
    Molecular weight: 23390.597 g/mol
    Composition:
       C: 1396
       H: 2540
       O: 254
