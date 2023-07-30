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
class FakeWangFilter(TextReplaceFilter):
    """Filter for Fake Wang authorities."""

    def __init__(self):
        super().__init__(
            r"(汪(精(卫|衛)|兆(铭|銘))|\[\[汪(精(卫|衛)|兆(铭|銘))\]\])(政权|政權)",
            r"汪伪政权",
        )

    @property
    def log(self) -> str:
        return "修正汪伪政权名称"


@register_filter
class FakeManchukuoFilter(TextReplaceFilter):
    """Filter for Fake Manchukuo authorities."""

    def __init__(self):
        super().__init__(
            r"([^伪僞偽])(滿|满)洲(国|國)",
            r"\1伪满洲国",
        )

    @property
    def log(self) -> str:
        return "修正伪满洲国名称"
