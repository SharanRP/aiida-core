###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Module for the calculation parameter type
"""

from .identifier import IdentifierParamType

__all__ = ('CalculationParamType',)


class CalculationParamType(IdentifierParamType):
    """The ParamType for identifying Calculation entities or its subclasses"""

    name = 'Calculation'

    @property
    def orm_class_loader(self):
        """Return the orm entity loader class, which should be a subclass of OrmEntityLoader. This class is supposed
        to be used to load the entity for a given identifier

        :return: the orm entity loader class for this ParamType
        """
        from aiida.orm.utils.loaders import CalculationEntityLoader

        return CalculationEntityLoader
