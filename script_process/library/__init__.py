from . import debugging
from . import data_structures
from . import transitions
from . import attacks
from . import inits
from . import sprites

DEPENDENCIES = (
        debugging.DEPENDENCIES
        + data_structures.DEPENDENCIES
        + transitions.DEPENDENCIES
        + attacks.DEPENDENCIES
        + inits.DEPENDENCIES
        + sprites.DEPENDENCIES
)
