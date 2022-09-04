import scanpy as sc
import sys

__version__ = "0.0.4"


def main():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)
    elif "--help" in sys.argv[1:]:
        print("h5adcat H5AD_FILE")
        exit(0)

    file = sys.argv[1]

    adata = sc.read(file)
    print(str(adata))


if __name__ == "__main__":
    main()