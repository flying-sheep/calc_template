import fastgenomics.io as fg_io
from anndata import AnnData

from . import paths, params


def get_summary(adata: AnnData):
    summary_params = ''.join(f' * {param}={val}\n' for param, val in fg_io.get_parameters().items())
    return f'''\
App description

### Results
App did things with the {params.param1name} parameter
on {len(adata.obs_names)} cells and {len(adata.var_names)} genes.

### Details
Explanation of what the app did why

### Parameters
{summary_params}
'''


def write_summary(adata: AnnData):
    with paths.summary.open('w') as f:
        f.write(get_summary(adata))
