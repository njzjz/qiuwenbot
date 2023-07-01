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
import os

from pywikibot import family


class QiuwenFamily(family.Family):
    """Qiuwen faimily."""

    name = "qiuwen"
    langs = {"zh": os.environ.get("QIUWEN_DOMAIN", "www.qiuwenbaike.cn")}

    def scriptpath(self, code):
        return ""

    def protocol(self, code):
        return "HTTPS"

    def isPublic(self):
        return False


family.Family._families["qiuwen"] = QiuwenFamily()
