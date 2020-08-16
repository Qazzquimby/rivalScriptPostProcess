from script_process.library import debugging
from script_process.library import data_structures
from script_process.library import transitions
from script_process.library import attacks
from script_process.library import inits

DEPENDENCIES = (
        debugging.DEPENDENCIES
        + data_structures.DEPENDENCIES
        + transitions.DEPENDENCIES
        + attacks.DEPENDENCIES
        + inits.DEPENDENCIES
)
