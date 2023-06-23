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
"""Filter texts."""
import importlib
from pathlib import Path

PACKAGE_BASE = "qiuwenbot.filter"
NOT_LOADABLE = ("__init__.py",)

for module_file in Path(__file__).parent.glob("*.py"):
    if module_file.name not in NOT_LOADABLE:
        module_name = f".{module_file.stem}"
        importlib.import_module(module_name, PACKAGE_BASE)
