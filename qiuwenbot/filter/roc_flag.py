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

from qiuwenbot.utils import devide_parameters, get_cat_regex, get_template_regex

from .common import get_comment
from .filter import Filter, register_filter


@register_filter
class ReplaceROCyear(Filter):
    """Filter to replace ROC flag from a string.

    Parameters
    ----------
    pattern : str
        Pattern to replace.
    repl : str
        Replacement.
    """

    def __init__(self):
        self.re_bd = get_template_regex(r"[Bb]d")
        self.re_year = re.compile(r"(?P<year>\d+)年")
        self.re_found = get_cat_regex(
            r"(?P<year>\d+)年(.*)(设立|建立|成立|创建|創建|設立|启用|啟用)(.*)"
        )
        self.re_event = get_cat_regex(r"(?P<year>\d+)年(台灣|台湾|台灣)(.*)")

        self.re_roc = re.compile(r"({{[\s]*ROC[\s]*}})")
        self.re_roc_flagicon = re.compile(r"({{[\s]*[Ff]lagicon[\s]*\|[\s]*ROC[\s]*}})")
        self.re_nationality = re.compile(
            r"\|[\s]*(國籍|国籍|[Nn]ationality)[\s]*=[\s]*({{[\s]*ROC[\s]*}})"
        )
        self.re_death_place = re.compile(
            r"\|[\s]*(逝世地點|逝世地点|[Dd]eath_place|[Pp]lace_of_death|[Rr]esting_place)[\s]*=[\s]*({{[\s]*ROC[\s]*}})"
        )
        self.re_death_place_flagicon = re.compile(
            r"\|[\s]*(逝世地點|逝世地点|[Dd]eath_place|[Pp]lace_of_death|[Rr]esting_place)[\s]*=[\s]*({{[\s]*flagicon[\s]*\|[\s]*ROC[\s]*}})"
        )

        self.comment = get_comment("replaced_flag 0")
        self.replaced_chn = r"{{CHN}}" + self.comment
        self.replaced_chn_flagicon = r"{{flagicon|CHN}}" + self.comment
        self.replaced_chn_nationality = r"|\1={{PRC-TWN}}" + self.comment
        self.replaced_chn_no_flag = r"|\1=[[中国]]" + self.comment
        self.replaced_death_place = r"|\1={{CHN}}" + self.comment
        self.replaced_death_place_flagicon = r"|\1={{flagicon|CHN}}" + self.comment

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
        yy = []
        replace_all = False
        replace_nationality = False
        replace_death = False
        replace_nationality_no_flag = False
        m_bd = self.re_bd.search(text)
        im_found = self.re_found.finditer(text)
        im_event = self.re_event.finditer(text)

        birth = None
        death = None
        if m_bd is not None:
            params = m_bd.group("params")
            params_dict = devide_parameters(params)
            birth = params_dict.get("1")
            death = params_dict.get("3", "living")

        if birth is not None:
            m_birth = self.re_year.search(birth)
            if m_birth is not None:
                y = m_birth.group("year")
                if int(y) > 1949:
                    # born after 1949
                    replace_all = True
                    replace_nationality = True

        if death is not None:
            m_death = self.re_year.search(death)
            if m_death is not None:
                y = m_death.group("year")
                if int(y) > 1949:
                    # death after 1949
                    replace_death = True
                    replace_nationality_no_flag = True
            elif death == "living":
                # living person
                replace_nationality_no_flag = True

        for m_found in im_found:
            y = m_found.group("year")
            yy.append(int(y))

        for m_event in im_event:
            y = m_event.group("year")
            yy.append(int(y))
        if len(yy) and min(yy) > 1949:
            replace_all = True
        if replace_nationality:
            # nationality
            text = self.re_nationality.sub(self.replaced_chn_nationality, text)
        if replace_nationality_no_flag:
            # nationality
            text = self.re_nationality.sub(self.replaced_chn_no_flag, text)
        if replace_death:
            text = self.re_death_place.sub(self.replaced_death_place, text)
            text = self.re_death_place_flagicon.sub(
                self.replaced_death_place_flagicon, text
            )
        if replace_all:
            text = self.re_roc.sub(self.replaced_chn, text)
            text = self.re_roc_flagicon.sub(self.replaced_chn_flagicon, text)
        return text

    @property
    def log(self) -> str:
        return "[[User:Njzjzbot/task1|清理台当局非法旗帜]]"
