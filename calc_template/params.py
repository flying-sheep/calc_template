from typing import Any, Callable

from fastgenomics.io import get_parameter


def check_param(param_name: str, dtype: type, check: Callable[[Any], bool], error: str) -> Any:
    param = get_parameter(param_name)
    try:
        param = dtype(param)
        assert check(param), error
    except AssertionError:
        raise ValueError(error)
    return param


param1name = check_param(
    'normalization', str, lambda p: True,
    f'Param 1 is wrong because stuff',
)
