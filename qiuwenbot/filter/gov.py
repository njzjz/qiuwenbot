# qiuwenbot, a bot to contribute to qiuwenbaike.cn
# Copyright (C) 2023  Jinzhe Zeng
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
class CNGovFilter(TextReplaceFilter):
    """Filter to fix the Chinese government terms."""

    def __init__(self):
        super().__init__(
            r"""(中国|中國|北京|中共)(当局|當局|政府)""",
            r"中国政府",
        )

    @property
    def log(self) -> str:
        return "修正涉政用语1"
