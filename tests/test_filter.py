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
from textwrap import dedent

from qiuwenbot.filter.filter import FilterChain, default_filters


def test_fileter():
    text = dedent(
        r"""\
        民国101年，日治時期“[[文化大革命]]”（[[文化大革命|文革]]）[[四人帮]]倒台后，
        [[蔡英文]][[中华民国总统|总统]]死了<ref>{{cite web|url=https://bbc.com/zhongwen/cywsl}}</ref>。
        <timeline>123</timeline>
        <score>456</score>
        <mapframe>789</mapframe>
        [[香港主權移交]]了！
        北京当局
        中华民国（台湾）
        中华民国台北市
        """
    )
    expected_text = dedent(
        r"""\
        2012年，日占時期“[[文化大革命]]”（“[[文化大革命|文革]]”）“[[四人帮]]”倒台后，
        [[蔡英文]]死了<!-- removed_ref site5 by njzjz/qiuwenbot -->。
        <!-- Removed timeline tag by njzjz/qiuwenbot -->
        <!-- Removed score tag by njzjz/qiuwenbot -->
        <!-- Removed mapframe tag by njzjz/qiuwenbot -->
        [[香港回归]]了！
        中国政府
        中国台湾
        中国台湾台北市
        """
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text


def test_roc_flag():
    text = dedent(
        r"""\
        {{ROC}}
        [[Category:1992年台灣]]
        """
    )
    expected_text = dedent(
        r"""\
        {{CHN}}<!-- replaced_flag 0 by njzjz/qiuwenbot -->
        [[Category:1992年台灣]]
        """
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text


def test_roc_flag2():
    text = dedent(
        r"""\
        {{bd|1992年}}{{ROC}}
        """
    )
    expected_text = dedent(
        r"""\
        {{bd|1992年}}{{CHN}}<!-- replaced_flag 0 by njzjz/qiuwenbot -->
        """
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text


def test_expired_template():
    date1 = datetime.today() - timedelta(days=60)
    date2 = datetime.today()

    text = (
        dedent(
            r"""\
        {{current|time=%s}}
        {{current|time=%s}}
        {{近期逝世|time=%s}}
        {{近期逝世|time=%s}}
        """
        )
        % (date1, date2, date1, date2)
    )
    expected_text = (
        dedent(
            r"""\
        {{current|time=%s}}
        {{近期逝世|time=%s}}
        """
        )
        % (date2, date2)
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text


def test_tw_univ():
    text = dedent(
        r"""\
        国立台湾大学
        国立阳明大学
        """
    )
    expected_text = dedent(
        r"""\
        台湾大学
        台湾阳明大学
        """
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text


def test_historical_authority():
    text = dedent(
        r"""\
        满洲国
        伪满洲国
        汪精卫政权
        清治时期
        """
    )
    expected_text = dedent(
        r"""\
        伪满洲国
        伪满洲国
        汪伪政权
        清朝时期
        """
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text


def test_tw_with_countries():
    text = dedent(
        r"""\
        '''123'''是台湾的。
        == 台湾 ==
        澳大利亚与台湾
        == 澳大利亚 ==
        台湾、澳大利亚
        == 香港 ==
        香港345
        [[委内瑞拉]]、[[台湾]]、[[比利時]]
        """
    )
    expected_text = dedent(
        r"""\
        '''123'''是台湾的。
        == 中国台湾 ==
        澳大利亚与中国台湾
        == 澳大利亚 ==
        中国台湾、澳大利亚
        == 中国香港 ==
        香港345
        [[委内瑞拉]]、中国台湾、[[比利時]]
        """
    )
    filter = FilterChain(default_filters)

    text = filter.filter(text)
    assert text == expected_text
