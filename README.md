# Make Delith structures - For thesis Chapter 3.3 - 3.4

Contains a messy script to remove sites from an ordered structure. Uses symmetry to reduce the total system size and the total number of crystals.

Makes no attempt at using Ewald summation at all...

## USAGE

Apparently this module requires enum.x (a fortran library that does some symmetry shit.), it's fairly simple to install, use conda if you want or just compile it from source...
[HERE.](github.com/msg-byu/enumlib).

Personally I ran the script, got the error pasted it in gpt and then let it fix the error.
I've not formatted outputs at all so it currently just spits a tonne of poscars...

This will restructure the unit cell to its minimal basis,
this is perhaps slightly annoying to then proceed to figure out what sites you've removed but im sure there is a utility out there.

### Using the example file

for all usage flags:
`python3 make_vacancies.py -h`
for a quick exmaple (using the poscar).

```py
python3 make_vacancies.py -s POSCAR -r Li -c 0.5 -n 150 -m 4 # should take seconds
python3 make_vacancies.py -s POSCAR -r Li -c 0.5 -n 1000 -m 16 # should take minutes
```

### Suggestions

I suggest cleaning up the input and output structures (with a fairly fuzzy symcalculator). In the case of the layered materials; i investigated o3-type, o2-type and p2-type, fd3m crystals. These crystal classes are exceedingly similar and alot of computational resources can be saved by just running all the resulting structures through a loose symmetry fit, the enum lib is good but even just reducing 10% of the structures by half will reduce compute load by 50%. This is especially important if allowing full cell relaxation.

Maybe a model pipeline would be.

1. sym reduce initial unvacant structures (removing those that are similar).
2. run this script at desired concentrations max sys sizes etc.
3. run cell to primitive cell on all structures (pymatgen builtin)
4. do a structure comparison of all resulting crystals (pymatgen buitlin) [StructureMatcher](https://pymatgen.org/pymatgen.analysis.html#pymatgen.analysis.structure_matcher.StructureMatcher)
5. run calculations on the small cells first. This will alert on any glaring issues and maybe help you identify errors of low interest. - massive positive formation if sum(Li-Li distances) ++

   a. (could use some Ewald sum to do similar things.)

6. postprocess by running a final symmetry calculation.

Alternatively, i believe there are complete cluster expansion codes that aim to do this fully automatically and may be of some interest.

- [ATAT](https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/manual.pdf)
- [CASM](https://prisms-center.github.io/CASMcode_docs/)
- [ICET](https://icet.materialsmodeling.org/)
