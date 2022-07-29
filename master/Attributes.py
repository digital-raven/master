import yaml

from master.TaskDate import TaskDate
from master.util.NoCompare import NoCompare


class Attributes(dict):
    """ Class to hold a Task's attributes.

    If a non-existent attribute is queried then a NoCompare is returned.

    This class also allows getting items in the dict via the dot operator.
    This means keys in this dict must be valid python3 identifiers.
    """
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    @classmethod
    def fromYaml(cls, s):
        """

        Args:
            s: String or filename of yaml to init from.
        Raises:
            FileNotFoundError or PermissionError if yaml was a file and
                couldn't be read.

            Whatever yaml.safe_load raises.
        """
        d = yaml.safe_load(s)
        if type(d) is str:
            with open(s) as f:
                s = f.read()
            d = yaml.safe_load(s)

        return Attributes(d)

    def toYamlDict(self):
        """ Reverses TaskDate to easymode yaml str.

        Necessary to dump this object as a yaml string.

            yaml.dump(attributes.toYamlDict)

        Returns:
            A dictionary that yaml can dump.
        """
        d = dict()
        d.update(self)
        for k, v in d.items():
            if 'date' in k:
                d[k] = str(v)

        return d

    def __getattr__(self, key):
        """ Expose keys as attributes.
        """
        if key in self.__dict__:
            return self.__dict__[key]

        return self.__getitem__(key)

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return NoCompare()

    def __setitem__(self, key, val):
        """ Keys must be python3 identifiers.

        Will also perform special parsing logic for keys that contain
        the word "date".
        """
        if not key.isidentifier():
            raise ValueError(f'The key "{key}" is not a valid identifier.')

        if type(key) is str and val:
            if 'date' in key:
                val = TaskDate(val)

        dict.__setitem__(self, key, val)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
