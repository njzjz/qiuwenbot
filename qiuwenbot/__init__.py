# set pywikibot environment
import os
os.environ['PYWIKIBOT_DIR']=os.path.dirname(__file__)

from .cleanrefs import main as clean_refs

__all__ = ['clean_refs']