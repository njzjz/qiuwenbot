# qiuwenbot, a bot to contribute to qiuwen.wiki
# Copyright (C) 2022  Jinzhe Zeng
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# set pywikibot environment
import tempfile
import shutil
import os

tmp_dir = tempfile.mkdtemp(prefix="qiuwenbot")
# copy user-config.py
shutil.copyfile(os.path.join(os.path.dirname(__file__), "user-config.py"), os.path.join(tmp_dir, "user-config.py"))
os.environ['PYWIKIBOT_DIR']=tmp_dir

from .cleanrefs import main as clean_refs
from .replaceroc import main as replace_roc
from .checkduplicated import main as check_duplicated_pages
from .removetimeline import main as remove_timeline
from .replaceyear import main as replace_year

__all__ = ['clean_refs', 'replace_roc', 'check_duplicated_pages', 'remove_timeline',
           'replace_year',
    ]
