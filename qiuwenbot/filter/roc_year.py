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

import cn2an

from .filter import Filter, register_filter


@register_filter
class ReplaceROCyear(Filter):
    """Filter to replace ROC year from a string.

    Parameters
    ----------
    pattern : str
        Pattern to replace.
    repl : str
        Replacement.
    """

    def __init__(self):
        self.re_roc_year = re.compile(
            r"(((\[\[([^\[\]]*\|)?(中(华|華))?民(国|國)\]\])|((中(华|華))?民(国|國)))(\d+|[一二三四五六七八九十]+)年)"
        )

    def filter(self, text: str) -> str:
        """Filter text.

        Parameters
        ----------
        text : str
            Text to filter.

        Returns
        -------
        str
            Filtered text.
        """
        # group 0 is the entire string, group -1 is the year
        matched = self.re_roc_year.findall(text)
        for mm in matched:
            try:
                roc_year = int(mm[-1])
            except ValueError:
                try:
                    roc_year = cn2an.cn2an(mm[-1])
                except ValueError:
                    continue
            # 38 - 1949; prevent conversion of 民国19xx年
            if roc_year > 38 and roc_year < 1000:
                ce_year = 1911 + roc_year
                entire_year_str = mm[0]
                ce_year_str = "%d年" % ce_year
                text = text.replace(entire_year_str, ce_year_str)
                # remove duplicate
                # first remove links
                text = text.replace("[[%s]]" % ce_year_str, ce_year_str)
                text = text.replace(f"{ce_year_str}（{ce_year_str}）", ce_year_str)
                text = text.replace(f"{ce_year_str}({ce_year_str})", ce_year_str)
                text = text.replace(f"{ce_year_str}（{str(ce_year)}）", ce_year_str)
                text = text.replace(f"{ce_year_str}({str(ce_year)})", ce_year_str)
        return text

    @property
    def log(self) -> str:
        return "[[User:Njzjzbot/task4|替换非法纪年]]"
