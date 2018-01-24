from pathlib import Path
from typing import Tuple

import pandas as pd
import scipy.sparse as sp
from anndata import AnnData


col_names = ['cell_id', 'entrez_id', 'expression']


def read_sparse_matrix(csv_file: Path) -> Tuple[sp.csr_matrix, pd.Index, pd.Index]:
    """ Reads a CSV-file into a scipy-sparse compressed sparse row format.

    :param csv_file: The tsv file containing the sparse input matrix
    :return: A scipy sparse matrix representing the data,
            the labels of the columns (genes), the labels of the cells (rows)
    """

    data = pd.read_csv(csv_file, sep=',', names=col_names, skiprows=1)
    gene_idx, gene_label = pd.factorize(data.entrez_id)
    cell_idx, cell_label = pd.factorize(data.cell_id)
    sp_mat = sp.coo_matrix((data.expression, (cell_idx, gene_idx)), dtype='float32')
    sp_mat_csr = sp_mat.tocsr()
    return sp_mat_csr, gene_label, cell_label


def read_data(csv_file: Path) -> AnnData:
    counts, genes, cells = read_sparse_matrix(csv_file)
    return AnnData(counts, dict(obs_names=cells), dict(var_names=genes))


def write_data(csv_file: Path, adata: AnnData):
    mat: sp.coo_matrix = adata.X.tocoo()
    cell_id   = adata.obs_names.values[mat.row]
    entrez_id = adata.var_names.values[mat.col]
    df = pd.DataFrame.from_dict(dict(
        cell_id=cell_id,
        entrez_id=entrez_id,
        expression=mat.data,
    ))
    df.to_csv(csv_file)

