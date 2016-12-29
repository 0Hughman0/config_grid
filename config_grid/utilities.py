from collections import namedtuple


Cell = namedtuple("Cell", ["row", "col", "value"])


class UniqueList(list):

    def is_new(self, new_value):
        if new_value in self:
            return False
        return True

    def check_still_unique(self):
        if len(self) == len(set(self)):
            return True
        return False

    def insert(self, i, x):
        if not self.is_new(x):
            raise ValueError("All new values must be unique")
        super().insert(i, x)

    def append(self, x):
        if not self.is_new(x):
            raise ValueError("All new values must be unique")
        super().append(x)


    def __iadd__(self, *args, **kwargs):
        val = super().__iadd__(*args, **kwargs)
        if val.check_still_unique():
            return val
        raise ValueError("All new values must be unique")

    def extend(self, t):
        super().extend(t)
        if not self.check_still_unique():
            raise ValueError("All new values must be unique")

    def __mul__(self, n):
        raise ValueError("This operator is not supported")

    def __init__(self, iterable=None):
        super().__init__(iterable)
        if not self.check_still_unique():
            raise ValueError("All new values must be unique")

    def __add__(self, y):
        val = super().__add__(y)
        if self.check_still_unique():
            return val
        raise ValueError("All new values must be unique")

    def __setitem__(self, i, y):
        if not self.is_new(y):
            raise ValueError("All new values must be unique")
        super().__setitem__(i, y)

    def swap(self, i, j):
        t1, self[i] = self[i], True
        t2, self[j] = self[j], False
        self[i] = t2
        self[j] = t1


class LineDict(dict):
    """
    Helper class for ConfigGrid

    Used to store data found in row/ columns, with strict order defined on init.

    Methods are the same as a normal dict, but with the ordering considered, apart from DIRECT ITERATION ITERATES OVER
    CONTENTS NOT KEYS.
    """
    def __init__(self, headings, default=""):
        assert isinstance(headings, list), "headings must be lists"
        super().__init__()
        self.headings = headings
        self.default = default

    def __setitem__(self, key, value):
        if key not in self.headings:
            raise KeyError("{} not found in Columns".format(key))
        return super().__setitem__(key, value)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if item not in self.headings:
                raise KeyError("{} not found in Columns".format(item))
            else:
                return self.default

    def __iter__(self):
        return (self[position] for position in self.headings)

    def keys(self):
        return self.headings

    def items(self):
        return zip(self.headings, iter(self))

    def values(self):
        return iter(self)

    def update(self, incoming_dict):
        if all(key in self.headings for key in incoming_dict.keys()):
            super().update(incoming_dict)
        else:
            raise KeyError("All keys in incoming_dict must also be in this dict")

    def copy(self):
        new_obj = LineDict(self.headings)
        new_obj.update(self.copy())
        return new_obj

    @staticmethod
    def fromkeys(keys, value=None):
        obj = LineDict(keys)
        filled_dict = super().fromkeys(keys, value)
        obj.update(filled_dict)
        return obj

    def setdefault(self, k, d=None):
        """
        Will try to return value of k. If k is not in LineDict, will add it, and add k to the end of headings.
        :param k: Key to be tried
        :param d: value to set at k if not found
        :return: value found at k (or d if k not found)
        """
        if k not in self.headings:
            raise KeyError("{} not found in Columns")
        return super().setdefault(k, d)

    def __repr__(self):
        return "LineDict {{{}}}".format(", ".join("{}: {}".format(key, value) for key, value in self.items()))

    def append(self, key, value):
        self.headings.append(key)
        self[key] = value
