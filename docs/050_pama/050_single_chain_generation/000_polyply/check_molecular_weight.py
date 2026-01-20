#!/usr/bin/env python3
"""
Compute molecular weight (molar mass) from a GROMACS .gro file.

Assumptions:
- Element is inferred from the atom name (first letter, or first two if valid).
- Works for standard organic/polymer systems (C, H, O, N, S, P, etc.).
"""

import sys
from collections import Counter

# Atomic weights in g/mol
ATOMIC_WEIGHTS = {
    "H": 1.00784,
    "C": 12.0107,
    "N": 14.0067,
    "O": 15.999,
    "S": 32.065,
    "P": 30.973761,
    "F": 18.998403,
    "Cl": 35.45,
    "Br": 79.904,
    "I": 126.90447,
}

def infer_element(atom_name):
    """
    Infer element from a GROMACS atom name.
    Examples:
      C1, C01  -> C
      H0A      -> H
      O09      -> O
      Cl1      -> Cl
    """
    atom_name = atom_name.strip()

    # Try two-character element first (e.g. Cl, Br)
    if len(atom_name) >= 2 and atom_name[:2].capitalize() in ATOMIC_WEIGHTS:
        return atom_name[:2].capitalize()

    # Fallback to first character
    return atom_name[0].capitalize()

def compute_molecular_weight(gro_file):
    element_counts = Counter()

    with open(gro_file, "r") as f:
        lines = f.readlines()

    # Skip title (line 0) and atom count (line 1)
    for line in lines[2:]:
        if len(line.strip()) == 0:
            continue

        # Box vector line is typically short
        if len(line.split()) <= 3:
            break

        atom_name = line[10:15].strip()
        element = infer_element(atom_name)

        if element not in ATOMIC_WEIGHTS:
            raise ValueError(f"Unknown element inferred from atom name '{atom_name}'")

        element_counts[element] += 1

    total_mass = sum(
        count * ATOMIC_WEIGHTS[element]
        for element, count in element_counts.items()
    )

    return total_mass, element_counts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: gro_molecular_weight.py <file.gro>")
        sys.exit(1)

    gro_file = sys.argv[1]
    mw, composition = compute_molecular_weight(gro_file)

    print(f"Molecular weight: {mw:.3f} g/mol")
    print("Composition:")
    for element, count in sorted(composition.items()):
        print(f"  {element:>2}: {count}")
