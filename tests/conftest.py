import sys
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch


HERE = Path(__file__).parent
APP_DIR = HERE.parent
DATA_DIR = APP_DIR / 'sample_data'


@pytest.fixture
def fg_env(monkeypatch: MonkeyPatch):
    for module_name in list(sys.modules.keys()):
        if module_name.startswith('fastgenomics'):
            del sys.modules[module_name]
    monkeypatch.setenv('FG_APP_DIR', str(APP_DIR))
    monkeypatch.setenv('FG_DATA_ROOT', str(DATA_DIR))


@pytest.fixture
def fg_env_clean(fg_env):
    import fastgenomics.io as fg_io

    for d in (fg_io.OUTPUT_DIR, fg_io.SUMMARY_DIR):
        for f in d.iterdir():
            if not f.name == '.gitignore':
                f.unlink()
