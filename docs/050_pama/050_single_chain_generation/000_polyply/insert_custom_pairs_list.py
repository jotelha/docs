#!/usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Replace the [ pairs ] section of an ITP file using pairs from a file"
    )
    parser.add_argument(
        "-p", "--pairs",
        default="python_pairs.dat",
        help="Input pairs file (default: python_pairs.dat)"
    )
    parser.add_argument(
        "-i", "--input",
        default="molecule_input.itp",
        help="Input ITP file (default: molecule_input.itp)"
    )
    parser.add_argument(
        "-o", "--output",
        default="molecule.itp",
        help="Output ITP file (default: molecule.itp)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational output"
    )

    args = parser.parse_args()

    # ----------------------------
    # Read new pairs
    # ----------------------------

    with open(args.pairs, "r") as f:
        new_pairs = [line.strip() for line in f if line.strip()]

    # ----------------------------
    # Read original ITP
    # ----------------------------

    with open(args.input, "r") as f:
        lines = f.readlines()

    # ----------------------------
    # Process file
    # ----------------------------

    in_pairs = False
    found_pairs_section = False
    output = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("[ pairs"):
            found_pairs_section = True
            in_pairs = True

            # Write header
            output.append(line)

            # Write new pairs (function type 1)
            for pair in new_pairs:
                parts = pair.split()
                if len(parts) >= 2:
                    output.append(f"{parts[0]:>6} {parts[1]:>6} 1\n")

            continue

        if in_pairs:
            if stripped.startswith("["):
                # End of [ pairs ] section
                in_pairs = False
                output.append(line)
            # Otherwise: skip old pairs content
            continue

        output.append(line)

    # ----------------------------
    # Append [ pairs ] if missing
    # ----------------------------

    if not found_pairs_section:
        output.append("\n[ pairs ]\n")
        for pair in new_pairs:
            parts = pair.split()
            if len(parts) >= 2:
                output.append(f"{parts[0]:>6} {parts[1]:>6} 1\n")

    # ----------------------------
    # Write output
    # ----------------------------

    with open(args.output, "w") as f:
        f.writelines(output)

    if not args.quiet:
        print(f"Wrote {len(new_pairs)} pairs to {args.output}")


if __name__ == "__main__":
    main()
