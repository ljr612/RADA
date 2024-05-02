# How to use: python igfold_use.py <H sequence> <L sequence> <protein name>

from igfold import IgFoldRunner
from igfold.refine.pyrosetta_ref import init_pyrosetta
import sys

init_pyrosetta()

H = sys.argv[1]
L = sys.argv[2]
name = sys.argv[3] + ".pdb"

sequences = {
    "H": H,
    "L": L
}
pred_pdb = name

igfold = IgFoldRunner()
out = igfold.fold(
    pred_pdb, # Output PDB file
    sequences=sequences, # Antibody sequences
    do_refine=True, # Refine the antibody structure with PyRosetta
    do_renum=True, # Renumber predicted antibody structure (Chothia)
)

out.prmsd # Predicted RMSD for each residue's N, CA, C, CB atoms (dim: 1, L, 4)