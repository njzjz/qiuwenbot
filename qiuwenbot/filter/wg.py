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
from .filter import TextReplaceFilter, register_filter


@register_filter
class WengeFilter(TextReplaceFilter):
    """Filter to add quote to Wen Ge."""

    def __init__(self):
        super().__init__(
            # not starts with quote
            # only replace links as there is something like 马文革
            r"([^“‘「『\[])((\[\[([^\[\]\|]+\|)?)(文革|文化大革命|四人帮)(\]\]))",
            r"\1“\2”",
        )

    @property
    def log(self) -> str:
        return "文革加引号"
