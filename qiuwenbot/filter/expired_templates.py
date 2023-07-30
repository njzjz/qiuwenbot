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
from datetime import datetime, timedelta

from qiuwenbot.filter.filter import Filter, register_filter
from qiuwenbot.utils import devide_parameters, get_template_regex


class RemoveExpiredTemplateFilter(Filter):
    """Filter to remove a certain tag.

    Parameters
    ----------
    tag : str
        Tag name to remove.
    """

    def __init__(self, template: str):
        self.template = template
        self.template_regex = get_template_regex(template, end=r"\s*")

    def filter(self, text: str) -> str:
        matched = self.template_regex.finditer(text)
        for mm in matched:
            rm = False
            params = mm.group("params")
            params_dict = devide_parameters(params)
            time = params_dict.get("time")
            if time is None:
                rm = True
            else:
                try:
                    isotime = datetime.fromisoformat(time)
                except ValueError:
                    rm = True
                else:
                    # a month ago
                    if (
                        isotime.timestamp()
                        < (datetime.now() - timedelta(days=31)).timestamp()
                    ):
                        rm = True
            if rm:
                text = text.replace(mm.group(0), "")
        return text

    @property
    def log(self) -> str:
        return f"移除已过期的[[Template:{self.template}|{self.template}]]模板"


@register_filter
class RemoveExpiredCurrentFilter(RemoveExpiredTemplateFilter):
    """Filter to remove {{current}}."""

    def __init__(self):
        super().__init__("current")


@register_filter
class RemoveExpiredDeadFilter(RemoveExpiredTemplateFilter):
    """Filter to remove {{近期逝世}}."""

    def __init__(self):
        super().__init__("近期逝世")


@register_filter
class RemoveExpiredDeadFilter2(RemoveExpiredTemplateFilter):
    """Filter to remove {{最近逝世}}."""

    def __init__(self):
        super().__init__("最近逝世")


@register_filter
class RemoveExpiredDeadFilter3(RemoveExpiredTemplateFilter):
    """Filter to remove {{recent death}}."""

    def __init__(self):
        super().__init__("recent death")
