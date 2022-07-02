import os
import logging

from .version import __version__

PACKAGEDIR = os.path.abspath(os.path.dirname(__file__))
name = 'sun'

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
LOG = logging.getLogger(__name__)

from .flares import Flares, read_lc_file