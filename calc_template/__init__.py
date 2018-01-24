from . import paths, params
from .data import read_data, write_data
from .summary import write_summary

import scanpy.api as sc


def main():
    adata = read_data(paths.exprs_in)

    # Do stuff with the anndata object, e.g.
    sc.pp.log1p(adata)

    write_data(paths.exprs_transformed, adata)
    write_summary(adata)
