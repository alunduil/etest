# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.


def bash_to_dict():
    '''Translate a BASH string into a python dictionary.

    Performs full parsing of BASH to generate a python dictionary whose keys are
    any variables set in the script and whose values are the appropriate values
    as set in the script (without variable interpolation).

    This parses in a type aware form that preserves the structure of strings,
    arrays, and nested types.

    Parameters
    ----------

    :``text``: Text to parse as BASH and extract a dictionary from.

    Returns
    -------

    Python dictionary whose keys are the set variables in the passed BASH.

    '''

    pass
