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
    """Filter to fix the Japanese authorities."""

    def __init__(self):
        super().__init__(
            r"日治(时期|時期)",
            r"日占\1",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语2"


@register_filter
class TWQingFilter(TextReplaceFilter):
    """Filter to fix the Qing authorities."""

    def __init__(self):
        super().__init__(
            r"清治(时期|時期)",
            r"清朝\1",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语2-2"


@register_filter
class TWUnivFilter1(TextReplaceFilter):
    """Filter to fix the name of unversities in the Taiwan area."""

    def __init__(self):
        super().__init__(
            r"(國立|国立)((臺|台)(灣|湾)((师范|師範|海洋|藝術|艺术|体育(运动)?|科技)?大(學|学)|戲曲學院|戏曲学院)|金门大学|金門大學)",
            r"\2",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语3"


@register_filter
class TWUnivFilter2(TextReplaceFilter):
    """Filter to fix the name of unversities in the Taiwan area."""

    def __init__(self):
        # only fix univ created after 1949
        super().__init__(
            r"(國立|国立)((高雄师范|高雄師範|彰化師範|彰化师范|台北艺术|臺北藝術|臺南|台南|體育|体育|阳明|陽明|阳明交通|陽明交通)大(学|學)|傳統藝術中心|传统艺术中心)",
            r"台湾\2",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语4"


@register_filter
class TWNameFilter1(TextReplaceFilter):
    """Filter to fix the name of the Taiwan area."""

    def __init__(self):
        super().__init__(
            r"((中华民国|中華民國)(\||\]\]\[\[)?(台|臺)(湾|灣)|(中华民国|中華民國)（(台|臺)(湾|灣)）)",
            r"中国台湾",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语5"


@register_filter
class TWNameFilter2(TextReplaceFilter):
    """Filter to fix the name of the Taiwan area."""

    def __init__(self):
        super().__init__(
            r"(中华民国|中華民國|\[\[中华民国\]\]|\[\[中華民國\]\])(臺北|台北|新北|桃园|桃園|台中|臺中|台南|臺南|高雄)",
            r"中国台湾\2",
        )

    @property
    def log(self) -> str:
        return "修正涉台用语6"
