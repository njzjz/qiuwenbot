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
from textwrap import dedent

from qiuwenbot.filter.filter import FilterChain, default_filters


def test_fileter():
    text = dedent(
        r"""
        民国101年，日治時期“[[文化大革命]]”（[[文化大革命|文革]]）后，
        [[蔡英文]][[中华民国总统|总统]]死了<ref>{{cite web|url=https://bbc.com/zhongwen/cywsl}}</ref>。
        <timeline>123</timeline>
        <score>456</score>
        <mapframe>789</mapframe>
    """[
            1:
        ]
    )
    expected_text = dedent(
        r"""
        2012年，日占時期“[[文化大革命]]”（“[[文化大革命|文革]]”）后，
        [[蔡英文]]死了<!-- removed_ref site5 by njzjz/qiuwenbot -->。
        <!-- Removed timeline tag by njzjz/qiuwenbot -->
        <!-- Removed score tag by njzjz/qiuwenbot -->
        <!-- Removed mapframe tag by njzjz/qiuwenbot -->
    """[
            1:
        ]
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text
