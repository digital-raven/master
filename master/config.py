""" Configuration related functions.
"""

import configparser
import os
from pathlib import Path
from master.util.edit import edit
from master.configs.default_ini import default_ini


user_confdir = '{}/.config/master'.format(Path.home())
user_conf = '{}/master.ini'.format(user_confdir)


def do_first_time_setup():
    """ First-time user setup for master.

    This copies the default.ini to the user's conf path. The user will be
    prompted to edit this configuration after it's copied.

    Raises:
        FileNotFoundError if the default config could not be read, or
        any of the exceptions raised by master.util.edit
    """
    os.makedirs(user_confdir, exist_ok=True)
    edit(default_ini, output_file=user_conf)


def add_config_args(args, config=None):
    """ Add params from a config file to an ArgumentParser.

    Parameters are only copied if not already set in the
    ArgumentParser.

    Args:
        args: ArgumentParser instance.
        config: Path to config file.

    Returns:
        namedtuple containing config parameters overridden by command
        line arguments.

    Raises:
        FileNotFoundError: Provided config file doesn't exist.
        KeyError: Configuration file has no default section (or no sections).
    """
    config = user_conf if not config else config

    if not os.path.exists(config):
        raise FileNotFoundError('Config {} does not exist.'.format(config))

    cp = configparser.ConfigParser()

    try:
        cp.read(config)
    except Exception as e:
        raise KeyError('Config "{}" is invalid. {}.'.format(config, e))

    if 'default' not in cp:
        raise KeyError('Your config at {config} has no "default" section. Did you touch that line during setup?')

    d = cp['default']

    # copy vals into args if not already in args.
    for key, val in d.items():
        try:
            if not getattr(args, key):
                setattr(args, key, val)
        except AttributeError:
            setattr(args, key, val)

    return args
