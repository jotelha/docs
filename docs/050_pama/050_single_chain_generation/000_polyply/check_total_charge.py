#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} molecule.itp")
    sys.exit(1)

itp_file = sys.argv[1]

total_charge = 0.0
in_atoms = False

print(f"Reading charges from: {itp_file}\n")

with open(itp_file) as f:
    for line in f:
        stripped = line.strip()

        # Enter [ atoms ] section
        if stripped.startswith("[ atoms ]"):
            in_atoms = True
            continue

        # Leave [ atoms ] section
        if in_atoms and stripped.startswith("["):
            break

        # Skip comments and blank lines
        if not in_atoms or not stripped or stripped.startswith(";"):
            continue

        fields = stripped.split()
        if len(fields) < 7:
            continue  # malformed atom line

        nr = fields[0]
        atom_name = fields[4]
        charge = float(fields[6])

        total_charge += charge
        print(f"Atom {nr:>4} ({atom_name:<4}): charge = {charge: .8f}")

print("\n---------------------------")
print(f"Total charge: {total_charge: .8f}")
