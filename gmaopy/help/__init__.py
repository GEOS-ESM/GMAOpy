from . import domains
from . import databases
from . import config
from . import datahook
from . import directivehelp
from . import statistics
from . import beauty
from .helpsystem import HelpSystem
from .asciiformatter import ASCIIFormatter

HelpSystem.register_formatter('ascii',ASCIIFormatter)
