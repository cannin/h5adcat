import sys
import argparse 
import scanpy as sc
import pandas as pd
import scipy.sparse as sp

__version__ = "0.0.14"


# def write_mtx(adata):
#     """Export AnnData object to mtx format
#     * Parameters
#         + adata : AnnData
#         An AnnData object

#         From: https://github.com/ebi-gene-expression-group/scanpy-scripts/blob/e53693336d8b37f0231d10d672b49c766d9c325b/scanpy_scripts/cmd_utils.py
#     """
#     mat = sp.coo_matrix(adata.X)

#     n_obs, n_var = mat.shape
#     n_entry = len(mat.data)

#     # Define the header lines as a Pandas DataFrame
#     header = pd.DataFrame(
#         ["%%MatrixMarket matrix coordinate real general", f"{n_var} {n_obs} {n_entry}"]
#     )
#     df = pd.DataFrame({"col": mat.col + 1, "row": mat.row + 1, "data": mat.data})

#     # Define outputs
#     mtx_fname = "matrix.mtx"
#     gene_fname = "genes.tsv"
#     barcode_fname = "barcodes.tsv"

#     # Write matrix with Pandas CSV
#     header.to_csv(mtx_fname, header=False, index=False, compression=None)
#     df.to_csv(mtx_fname, sep=" ", header=False, index=False, compression=None, mode="a")

#     # Now write the obs and var
#     obs_df = adata.obs.reset_index(level=0)
#     obs_df.to_csv(barcode_fname, sep="\t", header=False, index=False, compression=None)
#     var_df = adata.var.reset_index(level=0)
#     var_df.to_csv(gene_fname, sep="\t", header=False, index=False, compression=None)


def main():
    parser = argparse.ArgumentParser(description="Basic Information for .h5ad Files")

    parser.add_argument('-f', '--file', help='Input .h5ad File')
    parser.add_argument('-s', '--summary', default=True, action='store_false', help='Show Summary')
    parser.add_argument('-v', '--version', default=False, action='store_true', help='Show Version')
    parser.add_argument('-m', '--mtx', default=False, action='store_true', help='Convert to MTX')
    parser.add_argument('-q', '--qc', default=False, action='store_true', help='Make QC Plots')
    parser.add_argument('-d', '--data', default=False, action='store_true', help='Show Limited Data')

    parser.add_argument('-c', '--count_col', default='ncounts', help='N Count Column')
    parser.add_argument('-g', '--gene_col', default='ngenes', help='N Genes Column')
    parser.add_argument('-p', '--percent_mito_col', default='percent_mito', help='Percent Mitochondrion Column')

    if len(sys.argv)==1:
        parser.print_help() # Usage is too simplistic
        sys.exit(0)

    args = parser.parse_args()

    if args.version:
        print("h5adcat: " + __version__ + "\n\nDependencies: ")
        print(sc.logging.print_versions())
        sys.exit(0)

    # if args.help:
    #     parser.print_help()
    #     sys.exit(0)

    file = args.file

    adata = sc.read(file)

    if args.summary:
        print(str(adata))

    # if args.mtx:
    #     write_mtx(adata)

    if args.qc:
        sc.pl.highest_expr_genes(adata, n_top=10, show=False, save=".pdf") 
        sc.pl.violin(adata, [args.gene_col, args.count_col, args.percent_mito_col], jitter=0.4, multi_panel=True, show=False, save=".pdf")
        sc.pl.scatter(adata, x=args.count_col, y=args.percent_mito_col, show=False, save=".pdf")
        sc.pl.scatter(adata, x=args.count_col, y=args.gene_col, show=False, save=".pdf")

    if args.data: 
        print("X:\n")
        print(pd.DataFrame.sparse.from_spmatrix(adata.X).head(5))

        print("\nobs:\n")
        print(adata.obs.head(5))

        print("\nvar:\n")
        print(adata.var.head(5))


if __name__ == "__main__":
    main()

