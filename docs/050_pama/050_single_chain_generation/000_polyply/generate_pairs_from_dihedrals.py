#!/usr/bin/env python3

import argparse
import networkx as nx


# ----------------------------
# Generic section parser
# ----------------------------

def parse_section(itp, section, nfields):
    data = []
    in_section = False

    with open(itp) as f:
        for line in f:
            line = line.split(";")[0].strip()
            if not line:
                continue

            if line.startswith("["):
                in_section = line.lower().startswith(f"[ {section}")
                continue

            if in_section:
                fields = line.split()
                if len(fields) >= nfields:
                    data.append(tuple(map(int, fields[:nfields])))

    return data


# ----------------------------
# Parse nrexcl
# ----------------------------

def parse_nrexcl(itp):
    in_section = False

    with open(itp) as f:
        for line in f:
            stripped = line.strip()

            if stripped.lower().startswith("[ moleculetype"):
                in_section = True
                continue

            if in_section:
                if not stripped or stripped.startswith(";"):
                    continue

                fields = stripped.split()
                if len(fields) < 2:
                    raise RuntimeError("Invalid [ moleculetype ] entry")

                return int(fields[1])

    raise RuntimeError("nrexcl not found")


# ----------------------------
# Build bond graph
# ----------------------------

def build_bond_graph(bonds, constraints):
    G = nx.Graph()
    for i, j in bonds + constraints:
        G.add_edge(i, j)
    return G


# ----------------------------
# Generate GROMACS-equivalent pairs
# ----------------------------

def generate_pairs_from_dihedrals(G, dihedrals):
    """
    GROMACS logic (nrexcl = 3 case):

    - Automatic [ pairs ] are generated ONLY from dihedrals
    - Candidate pair = (first atom, fourth atom)
    - Pair is kept if shortest bond-path distance == 3
    """

    pairs = set()

    for i, j, k, l in dihedrals:
        try:
            d = nx.shortest_path_length(G, i, l)
        except nx.NetworkXNoPath:
            continue

        if d == 3:
            pairs.add(tuple(sorted((i, l))))

    return sorted(pairs)


# ----------------------------
# Main
# ----------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate GROMACS-equivalent [ pairs ] from an ITP file"
    )
    parser.add_argument(
        "-i", "--input",
        default="molecule_input.itp",
        help="Input ITP file (default: molecule_input.itp)"
    )
    parser.add_argument(
        "-o", "--output",
        default="python_pairs.dat",
        help="Output pairs file (default: python_pairs.dat)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational output"
    )

    args = parser.parse_args()

    itp = args.input
    out = args.output

    bonds = parse_section(itp, "bonds", 2)
    constraints = parse_section(itp, "constraints", 2)
    dihedrals = parse_section(itp, "dihedrals", 4)
    nrexcl = parse_nrexcl(itp)

    if not args.quiet:
        print(f"Parsed {len(bonds)} bonds")
        print(f"Parsed {len(constraints)} constraints")
        print(f"Parsed {len(dihedrals)} dihedrals")
        print(f"nrexcl = {nrexcl}")

        if nrexcl != 3:
            print("WARNING: script assumes nrexcl = 3")

    G = build_bond_graph(bonds, constraints)
    pairs = generate_pairs_from_dihedrals(G, dihedrals)

    if not args.quiet:
        print(f"\nGenerated {len(pairs)} GROMACS-equivalent pairs")
        print("\nFirst 20 pairs:")
        for p in pairs[:20]:
            print(p)

    with open(out, "w") as f:
        for i, j in pairs:
            f.write(f"{i} {j}\n")


if __name__ == "__main__":
    main()
