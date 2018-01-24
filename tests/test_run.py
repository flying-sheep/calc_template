from pathlib import Path
from shutil import which
from subprocess import run

import pytest


dir_data = Path(__file__).parent.parent / 'sample_data'
path_exprs_norm = dir_data / 'output' / 'expression.csv'
path_summary = dir_data / 'summary' / 'summary.md'


def test_run_locally(fg_env_clean):
    from calc_template import main, paths

    assert path_exprs_norm == paths.exprs_transformed
    assert path_summary == paths.summary
    assert not paths.exprs_transformed.is_file()
    assert not paths.summary.is_file()

    main()

    assert paths.exprs_transformed.is_file()
    assert paths.summary.is_file()


@pytest.mark.skipif(which('docker-compose') is None, reason='docker-compose not installed')
@pytest.mark.skipif(Path('/.dockerenv').is_file(), reason='We are inside of a Docker container')
def test_run_docker(fg_env_clean):
    assert not path_exprs_norm.is_file()
    assert not path_summary.is_file()

    run('docker-compose up --force-recreate --build --exit-code-from ci_integration_tests --abort-on-container-exit'.split())
    run('docker-compose down'.split())

    assert path_exprs_norm.is_file()
    assert path_summary.is_file()
