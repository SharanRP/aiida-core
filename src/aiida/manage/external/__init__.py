###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""User facing APIs to control AiiDA from the verdi cli, scripts or plugins"""

# AUTO-GENERATED

# fmt: off

from .rmq import *

__all__ = (
    'BROKER_DEFAULTS',
    'ManagementApiConnectionError',
    'RabbitmqManagementClient',
    'get_launch_queue_name',
    'get_message_exchange_name',
    'get_rmq_url',
    'get_task_exchange_name',
)

# fmt: on
