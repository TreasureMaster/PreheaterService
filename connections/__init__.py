# from .lindevice import LINDevice
# from .pyLIN import LIN
from .pyLIN import LIN_REVISIONS_NAMES, LIN_REVISIONS_BUSES
from .linconnection import LINConnection


__all__ = [
    # 'LIN',
    'LIN_REVISIONS_NAMES',
    'LIN_REVISIONS_BUSES',
    'LINConnection'
]