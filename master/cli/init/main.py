import os
import sys
from importlib import import_module

from master.Attributes import Attributes
from master.Project import Project
from master.util.edit import edit


def do_init(args):

    # Determine base config string
    conf = args.conf
    templates = ['agile', 'basic', 'calendar', 'note']
    if os.path.exists(conf):
        with open(conf) as f:
            conf = f.read()
    elif conf in templates:
        conf = import_module(f'master.configs.{conf}').__dict__[conf]
    else:
        t = ', '.join(templates)
        print(f'ERROR: The conf {conf} is not a file nor is it a template in {t}.')
        sys.exit(1)

    # Init project with basic config. This will perform text-replacement.
    try:
        p = Project.initOnDisk(args.path, args.username, conf=conf, force=args.force)
    except FileExistsError as e:
        print('ERROR:', e, 'Run with "--force" to re-init.')
        sys.exit(1)
    except FileNotFoundError as e:
        print('ERROR: master cannot init in non-existent nested directories.')
        sys.exit(1)
    except ValueError as e:
        print(f'ERROR: Config file {args.conf} is invalid yaml: {e}')
        sys.exit(1)

    # Read config back
    with open(f'{p.path}/project.yaml') as f:
        conf = f.read()
    conf = edit(conf)

    try:  # Edit the conf and save to project
        # Test validity of yaml
        _ = Project('dontcare', args.path, None, None, Attributes.fromYaml(conf))

        # Write config
        with open(f'{p.path}/project.yaml', 'w') as f:
            f.write(conf)
    except Exception as e:  # Should catch file io errors.
        print(f'ERROR: Initializing project: {e}')
        bkp = f'{args.conf}.yaml.bkp'
        try:
            with open(bkp, 'w') as f:
                f.write(conf)
            print(f'Backup config saved to {bkp}')
        except Exception as e:
            print(f'No config backup could be saved: {e}.')

        sys.exit(1)
