""" Manage projects and tasks.
"""
import os
import tempfile
from subprocess import call


def edit(s = '', output_file='', editor=''):
    """ Open a string in a text editor.

    If output_file is supplied, then the string will be copied to that file.

    Returns:
        The text from the edited file.

    Raises:
        ValueError if the editor wasn't set and neither were the VISUAL or
        EDITOR environment variables.

        PermissionError if the file could not be edited.
    """
    if not editor:
        if 'EDITOR' in os.environ:
            editor = os.environ['EDITOR']
        elif 'VISUAL' in os.environ:
            editor = os.environ['VISUAL']

    if not editor:
        raise ValueError('Neither the "VISUAL" or "EDITOR" environment variables had values.')

    _, path = tempfile.mkstemp(suffix='.rst')

    try:
        with open(path, 'w') as f:
            f.write(s)

        call([editor, path])

        with open(path, 'r') as f:
            text = f.read()

    finally:
        os.remove(path)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(text)

    return text
