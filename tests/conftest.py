from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

HERE = Path(__file__).parent
APP_DIR   = HERE.parent
DATA_ROOT = APP_DIR / 'sample_data'


local_paths = dict(
    app=APP_DIR,
    data=DATA_ROOT / 'data',
    config=DATA_ROOT / 'config',
    summary=DATA_ROOT / 'summary',
    output=DATA_ROOT / 'output',
)


@pytest.fixture
def app_dir():
    return APP_DIR


@pytest.fixture
def data_root():
    return DATA_ROOT


@pytest.fixture
def local(monkeypatch: MonkeyPatch):
    """patches the paths for local testing"""
    monkeypatch.setattr('fastgenomics.common.DEFAULT_APP_DIR', str(APP_DIR))
    monkeypatch.setattr('fastgenomics.common.DEFAULT_DATA_ROOT', str(DATA_ROOT))
    monkeypatch.setattr('fastgenomics.common._PATHS', local_paths)
    monkeypatch.setattr('fastgenomics.common._PARAMETERS', None)


@pytest.fixture
def clear_output():
    """clear everything except of .gitignore"""
    for name in ['output', 'summary']:
        sub_dir = DATA_ROOT / name
        for entry in sub_dir.glob('*.*'):
            if entry.name != '.gitignore':
                entry.unlink()
