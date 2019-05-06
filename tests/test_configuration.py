import pytest
from youvlog.configuration import get_app_home
from youvlog.exceptions import EnvironmentVariableError


def test_get_app_home():
    with pytest.raises(EnvironmentVariableError):
        get_app_home()

