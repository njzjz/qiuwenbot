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
import re

try:
    import importlib.resources as pkg_resources
except ImportError:
    # python < 3.7
    import importlib_resources as pkg_resources

import qiuwenbot.filter

from .common import get_comment
from .filter import Filter, register_filter


@register_filter
class CleanRefsFilter(Filter):
    """Filter to clean references."""

    def __init__(self):
        """Initialize the filter."""
        self.rerefs = re.compile(r"(?is)<ref(?P<params>[^>/]*)>(?P<content>.*?)</ref>")
        self.removed_urls = pkg_resources.read_text(
            qiuwenbot.filter, "ref_blacklist.txt"
        ).splitlines()

    def filter(self, text: str) -> str:
        for match in self.rerefs.finditer(text):
            ref = match.group("content")
            removed = tuple(url in str(ref) for url in self.removed_urls)
            try:
                ii = removed.index(True)
            except ValueError:
                continue
            else:
                text = text.replace(
                    match.group(), get_comment("removed_ref site%d" % (ii,))
                )
        return text

    @property
    def log(self) -> str:
        return "[[User:Njzjzbot/task0|清理非法参考文献]]"
