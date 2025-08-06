import os
import argparse
from pymatgen.core import Structure
from pymatgen.transformations.standard_transformations import (
    SubstitutionTransformation, RemoveSpeciesTransformation
)
from pymatgen.transformations.advanced_transformations import EnumerateStructureTransformation


def generate_enum_structures(structure_path: str, stripped_species: str, max_cell_size: int,
                             conc: float, num_structures: int, output_dir: str, symm_prec: float = 0.1):
    structure = Structure.from_file(structure_path)
    remove_species = RemoveSpeciesTransformation(["Tc"])  # "Tc" used as dummy placeholder

    # Create disordered structure by partial substitution
    substitution = SubstitutionTransformation({stripped_species: {stripped_species: conc, "Tc": 1 - conc}})
    substituted = substitution.apply_transformation(structure)

    enumerator = EnumerateStructureTransformation(
        sort_criteria="nsites", min_cell_size=1, max_cell_size=max_cell_size, symm_prec=symm_prec
    )
    # remove the Tc.
    result_list = enumerator.apply_transformation(substituted, return_ranked_list=num_structures)

    for idx, result in enumerate(result_list):
        struct = remove_species.apply_transformation(result["structure"])
        conc_str = f"{conc:.2f}".replace('.', 'p')
        filename = f"{conc_str}_{idx}.vasp"
        filepath = os.path.join(output_dir, filename)
        os.makedirs(output_dir, exist_ok=True)
        struct.to(filename=filepath, fmt="poscar")


def main():
    parser = argparse.ArgumentParser(description="Generate enumerated structures with vacancies/substitutions.")
    parser.add_argument("-s", "--structure", type=str, required=True, help="Path to input structure (e.g. CONTCAR)")
    parser.add_argument("-r", "--remove", type=str, required=True, help="Species to substitute (e.g., Li)")
    parser.add_argument("-m", "--maxsize", type=int, default=4, help="Maximum supercell size to search")
    parser.add_argument("-n", "--numstrucs", type=int, default=150, help="Maximum number of structures to generate")
    parser.add_argument("-c", "--conc", type=float, default=0.5, help="Target concentration of retained species.")
    parser.add_argument("--output", type=str, default="./res/", help="Base output directory")

    parser.add_argument("--symmprec", type=float, default=0.1, help="symmetry value to use,\
         note this is different to the enum prec param. Since a general scope is more important\
             this can probably be loose than it is.")

    args = parser.parse_args()
    generate_enum_structures(
        structure_path=args.structure,
        stripped_species=args.remove,
        max_cell_size=args.maxsize,
        conc=args.conc,
        num_structures=args.numstrucs,
        output_dir=args.output,
        symm_prec=args.symmprec
    )

if __name__ == "__main__":
    main()
