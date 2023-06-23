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
from .common import get_comment
from .filter import TextReplaceFilter, register_filter


class RemoveTagFilter(TextReplaceFilter):
    """Filter to remove a certain tag.

    Parameters
    ----------
    tag : str
        Tag name to remove.
    """

    def __init__(self, tag: str):
        self.tag = tag
        super().__init__(
            r"(?is)<{tag}(?P<params>[^>/]*)>(?P<content>.*?)</{tag}>".format(tag=tag),
            get_comment(rf"Removed {tag} tag"),
        )

    @property
    def log(self) -> str:
        return f"[[User:Njzjzbot/task3|移除{self.tag}标签]]"


@register_filter
class RemoveTimelineFilter(RemoveTagFilter):
    """Filter to remove timeline tag."""

    def __init__(self):
        super().__init__("timeline")


@register_filter
class RemoveScoreFilter(RemoveTagFilter):
    """Filter to remove score tag."""

    def __init__(self):
        super().__init__("score")


@register_filter
class RemoveMapframeFilter(RemoveTagFilter):
    """Filter to remove mapframe tag."""

    def __init__(self):
        super().__init__("mapframe")
