"""
Base Configuration
"""

import os
from collections import namedtuple
from configparser import ConfigParser

from youvlog.exceptions import EnvironmentVariableError


def get_app_home():
    app_home = os.environ.get('APP_HOME', None)
    if not app_home:
        raise EnvironmentVariableError('APP_HOME is not exist.')
    return app_home


class Config(object):
    def __init__(self, app_home, file_name):
        self.config_parse = ConfigParser()

        self.app_home = app_home

        config_name = self._get_config_file(file_name)
        self.config_parse.read(config_name)

    def _get_config_file_from_default(self, file_name):
        templates_dir = os.path.join(os.path.dirname(__file__),
                                     'config_templates')
        file_path = os.path.join(templates_dir, file_name)
        return file_path

    def _get_config_file_from_env(self, file_name):
        app_home = self.app_home
        file_path = os.path.join(app_home, file_name)
        return file_path

    def _get_config_file(self, file_name):
        try:
            file_path = self._get_config_file_from_env(file_name)
        except EnvironmentVariableError:
            default_file_name = '_'.join(('default', file_name))
            file_path = self._get_config_file_from_default(default_file_name)
        return file_path

    def parse_config(self, **kwargs):
        sections = self.config_parse.sections()

        configs = {}

        for section in sections:
            items = self.config_parse.items(section, **kwargs)
            config_dict = {name: value for name, value in items}

            config = namedtuple(section, list(config_dict.keys()))
            config(**config_dict)
            configs[section] = config

        return configs


APP_HOME = get_app_home()

_app_config_instance = Config(APP_HOME, 'app.ini')
app_config = _app_config_instance.parse_config(raw=True)
