import sys
import argparse 
from argparse import RawTextHelpFormatter
import scanpy as sc
import pandas as pd
import scipy.sparse as sp
from h5adcat import __version__
import io
from contextlib import redirect_stdout

s = io.StringIO()
with redirect_stdout(s):
    sc.logging.print_versions()
__version_str__ = "Session Info:\n" + s.getvalue()


def write_mtx(adata):
   #print("MTX\n")
    """Export AnnData object to mtx format
    * Parameters
        + adata : AnnData
        An AnnData object

        Simplification From: https://github.com/ebi-gene-expression-group/scanpy-scripts/blob/develop/scanpy_scripts/cmd_utils.py
    """
    mat = sp.coo_matrix(adata.X)

    n_obs, n_var = mat.shape
    n_entry = len(mat.data)

    # Define the header lines as a Pandas DataFrame
    header = pd.DataFrame(
        ["%%MatrixMarket matrix coordinate real general", f"{n_var} {n_obs} {n_entry}"]
    )
    df = pd.DataFrame({"col": mat.col + 1, "row": mat.row + 1, "data": mat.data})

    # Define outputs
    mtx_fname = "matrix.mtx"
    gene_fname = "genes.tsv"
    barcode_fname = "barcodes.tsv"

    # Write matrix with Pandas CSV
    header.to_csv(mtx_fname, header=False, index=False, compression=None)
    df.to_csv(mtx_fname, sep=" ", header=False, index=False, compression=None, mode="a")

    # Now write the obs and var
    obs_df = adata.obs.reset_index(level=0)
    obs_df.to_csv(barcode_fname, sep="\t", header=False, index=False, compression=None)
    var_df = adata.var.reset_index(level=0)
    var_df.to_csv(gene_fname, sep="\t", header=False, index=False, compression=None)


def main():
    parser = argparse.ArgumentParser(description="Basic Information for single-cell RNAseq (scRNAseq) .h5ad Files and Conversion to MTX", formatter_class=RawTextHelpFormatter)

    parser.add_argument('file', help='Input .h5ad File')
    parser.add_argument('-v', '--version', action='version', version=__version_str__)
    parser.add_argument('-m', '--mtx', default=False, action='store_true', help='convert to sparse matrix format (MTX)')
    parser.add_argument('-d', '--data', default=False, action='store_true', help='show limited data rows')
    #parser.add_argument('-s', '--summary', default=False, action='store_true', help='Show Summary')

    #parser.add_argument('-q', '--qc', default=False, action='store_true', help='make quality control plots')
    #parser.add_argument('-c', '--count_col', default='ncounts', help='N Count Column')
    #parser.add_argument('-g', '--gene_col', default='ngenes', help='N Genes Column')
    #parser.add_argument('-p', '--percent_mito_col', default='percent_mito', help='Percent Mitochondrion Column')

    if len(sys.argv)==1:
        parser.print_help() # Usage is too simplistic
        sys.exit(0)

    args = parser.parse_args()

    file = args.file

    adata = sc.read_h5ad(file)
    
    # Display basic information
    if not args.mtx and not args.data:
        print(str(adata) + "\n")

    if args.mtx:
        write_mtx(adata)

    if args.data: 
        print("X Head:\n")
        print(pd.DataFrame.sparse.from_spmatrix(adata.X).head(5))

        print("\nobs Head:\n")
        print(adata.obs.head(5))

        print("\nvar Head:\n")
        print(adata.var.head(5))

    #if args.qc:
    #    sc.pl.highest_expr_genes(adata, n_top=10, show=False, save=".svg") 
        # sc.pl.violin(adata, [args.gene_col, args.count_col, args.percent_mito_col], jitter=0.4, multi_panel=True, show=False, save=".pdf")
        # sc.pl.scatter(adata, x=args.count_col, y=args.percent_mito_col, show=False, save=".pdf")
        # sc.pl.scatter(adata, x=args.count_col, y=args.gene_col, show=False, save=".pdf")


if __name__ == "__main__":
    main()

