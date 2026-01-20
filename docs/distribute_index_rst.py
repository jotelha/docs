from pathlib import Path

ROOT = Path(".")

INDEX_CONTENT = """
.. include:: README.md
   :parser: myst_parser.sphinx_

.. toctree::
   :maxdepth: 1
   :glob:

   */index

"""

for path in ROOT.rglob("*"):
    if not path.is_dir():
        continue

    # Skip build and hidden directories
    if path.name.startswith(".") or path.name == "_build":
        continue

    index_file = path / "index.rst"
    index_file.write_text(INDEX_CONTENT, encoding="utf-8")

print("index.rst files written.")
