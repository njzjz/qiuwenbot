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
"""Qiuwen bot."""
# set pywikibot environment
import os
import shutil
import tempfile

tmp_dir = tempfile.mkdtemp(prefix="qiuwenbot")
# copy user-config.py
shutil.copyfile(
    os.path.join(os.path.dirname(__file__), "user-config.py"),
    os.path.join(tmp_dir, "user-config.py"),
)
os.environ["PYWIKIBOT_DIR"] = tmp_dir

import qiuwenbot.qwfamily  # noqa: F401, I001
