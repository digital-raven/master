import os
import sys
from importlib import import_module
from pathlib import Path

from libzet import Attributes

from master.Project import Project
from master.util.edit import edit


def do_init(args):

    # Determine base config string
    template = args.template
    templates = ['agile', 'calendar', 'task', 'note']
    if os.path.exists(template):
        with open(template) as f:
            template = f.read()
    elif template in templates:
        template = import_module(f'master.configs.{template}').__dict__[template]
    else:
        t = ', '.join(templates)
        print(f'ERROR: The template {template} is not a file nor is it a template in {t}.')
        sys.exit(1)

    # Init project with basic config.
    try:
        p = Project.initOnDisk(args.path, template, args.force)
    except FileExistsError as e:
        print('ERROR:', e, 'Run with "--force" to re-init.')
        sys.exit(1)
    except FileNotFoundError as e:
        print('ERROR: master cannot init in non-existent nested directories.')
        sys.exit(1)
    except ValueError as e:
        print(f'ERROR: Config file {args.template} is invalid yaml: {e}')
        sys.exit(1)

    # Read config back
    with open(f'{args.path}/ztemplate.yaml') as f:
        template = f.read()

    template = edit(template)

    try:
        # Test validity of yaml
        Attributes.fromYaml(template)

        # Write config
        with open(f'{args.path}/ztemplate.yaml', 'w') as f:
            f.write(template)
    except OSError as e:  # Should catch file io errors.
        print(f'ERROR: Initializing project: {e}')
        bkp = f'ztemplate.yaml.bkp'
        try:
            with open(bkp, 'w') as f:
                f.write(template)
            print(f'Backup config saved to {bkp}')
        except Exception as e:
            print(f'No config backup could be saved: {e}.')

        sys.exit(1)
