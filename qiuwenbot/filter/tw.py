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
class TWLeaderFilter(TextReplaceFilter):
    """Filter to fix the leader name in the Taiwan area."""

    def __init__(self):
        super().__init__(
            # not starts with quote
            (
                r"((\[\[)?(蒋介石|蒋中正|严家淦|蒋经国|李登辉|陈水扁|蔡英文|蔣介石|蔣中正|嚴家淦|蔣經國|李登輝|陳水扁)(\]\])?)"
                r"((\[\[([^\|\[\]]+\|)?)?(總統|总统)(\]\])?)"
            ),
            r"\1",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语1"


@register_filter
class TWJPFilter(TextReplaceFilter):
    """Filter to fix the leader name in the Taiwan area."""

    def __init__(self):
        super().__init__(
            # not starts with quote
            r"日治(时期|時期)",
            r"日占\1",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语2"
