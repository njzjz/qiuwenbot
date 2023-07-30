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
from typing import Dict

import pywikibot
from pywikibot.textlib import ignore_case

from .bot import get_page


def archieve_page(page: pywikibot.Page, site: pywikibot.Site) -> pywikibot.Page:
    """Archieve a page.

    Parameters
    ----------
    page: pywikibot.Page
        page to archieve
    site: pywikibot.Site
        qiuwen site

    Returns
    -------
    pywikibot.Page
        page with old title
    """
    ii = 1
    oldtitle = page.title()
    while True:
        title = oldtitle + "/存档%d" % ii
        if title:
            archieve_page = get_page(title, site)
            if not archieve_page.exists():
                page.text = page.text.replace("{{Archives}}", "")
                page.save("删除archieves模板")
                page.move(title, "存档")
                oldpage = get_page(oldtitle, site)
                oldpage.text = "{{Archives}}"
                oldpage.save("加入archieves模板")
                return oldpage
        ii += 1


def get_cat_regex(name: str = r"[^\[\]]+") -> re.Pattern:
    """Get categories regex.

    Parameters
    ----------
    name : str, optional
        Name or regex of the category, by default all categories.

    Returns
    -------
    List[str]
        Categories.
    """
    namespaces = [ignore_case("Category"), ignore_case("分類"), ignore_case("分类")]
    return re.compile(
        r"\[\[ *(?P<namespace>{namespace})\s*:(?P<name>{name})\]\]".format(
            name=name, namespace="|".join(namespaces)
        )
    )


def get_template_regex(name: str = r"[^{\|#0-9][^{\|#]*?", end: str = "") -> re.Pattern:
    """Get templates regex.

    Parameters
    ----------
    name : str, optional
        Name or regex of the template, by default all templates.
    end : str, optional
        End of the template, by default "".

    Returns
    -------
    List[str]
        Templates.
    """
    return re.compile(
        rf"""
        {{{{\s*(?:msg:\s*)?
        (?P<name>({name}))\s*
        (?:\|(?P<params> [^{{]*?
                (({{{{{{[^{{}}]+?}}}}}}
                    |{{{{[^{{}}]+?}}}}
                    |{{[^{{}}]*?}}
                ) [^{{]*?
                )*?
            )?
        )?
        }}}}{end}
        """,
        re.VERBOSE | re.DOTALL,
    )


def devide_parameters(params: str) -> Dict[str, str]:
    """Devide parameters and remove subtemplate in it.

    Parameters
    ----------
    params : str
        parameter string

    Returns
    -------
    Dict[str, str]
        dict of params
    """
    if params is None:
        return {}
    # detect | in another template
    regex_template = get_template_regex()
    params = regex_template.sub("", params)
    params_dict = {}
    for ii, param in enumerate(params.split("|"), 1):
        if "=" in param:
            key, value = param.split("=", 1)
            params_dict[key.strip()] = value.strip()
        else:
            params_dict[str(ii)] = param.strip()
    return params_dict


coutries = [
    "阿富汗",
    "阿尔巴尼亚",
    "阿尔及利亚",
    "安道尔",
    "安哥拉",
    "安提瓜和巴布达",
    "阿根廷",
    "亚美尼亚",
    "澳大利亚",
    "奥地利",
    "阿塞拜疆",
    "巴哈马",
    "巴林",
    "孟加拉国",
    "巴巴多斯",
    "白俄罗斯",
    "比利时",
    "伯利兹",
    "贝宁",
    "不丹",
    "玻利维亚",
    "波斯尼亚和黑塞哥维那",
    "博茨瓦纳",
    "巴西",
    "文莱",
    "保加利亚",
    "布基纳法索",
    "布隆迪",
    "柬埔寨",
    "喀麦隆",
    "加拿大",
    "佛得角",
    "中非共和国",
    "乍得",
    "智利",
    "中国",
    "哥伦比亚",
    "科摩罗",
    "刚果（布）",
    "刚果（金）",
    "哥斯达黎加",
    "科特迪瓦",
    "克罗地亚",
    "古巴",
    "塞浦路斯",
    "捷克",
    "朝鲜",
    "丹麦",
    "吉布提",
    "多米尼加",
    "厄瓜多尔",
    "埃及",
    "萨尔瓦多",
    "赤道几内亚",
    "厄立特里亚",
    "爱沙尼亚",
    "埃塞俄比亚",
    "斐济",
    "芬兰",
    "法国",
    "加蓬",
    "冈比亚",
    "格鲁吉亚",
    "德国",
    "加纳",
    "希腊",
    "格林纳达",
    "危地马拉",
    "几内亚",
    "几内亚比绍",
    "圭亚那",
    "海地",
    "洪都拉斯",
    "匈牙利",
    "冰岛",
    "印度",
    "印度尼西亚",
    "伊朗",
    "伊拉克",
    "爱尔兰",
    "以色列",
    "意大利",
    "牙买加",
    "日本",
    "约旦",
    "哈萨克斯坦",
    "肯尼亚",
    "科索沃",
    "科威特",
    "吉尔吉斯斯坦",
    "老挝",
    "拉脱维亚",
    "黎巴嫩",
    "莱索托",
    "利比里亚",
    "利比亚",
    "立陶宛",
    "卢森堡",
    "马其顿",
    "马达加斯加",
    "马拉维",
    "马来西亚",
    "马尔代夫",
    "马里",
    "马耳他",
    "毛里塔尼亚",
    "毛里求斯",
    "墨西哥",
    "摩尔多瓦",
    "蒙古",
    "黑山",
    "摩洛哥",
    "莫桑比克",
    "缅甸",
    "纳米比亚",
    "尼泊尔",
    "荷兰",
    "新西兰",
    "尼加拉瓜",
    "尼日尔",
    "尼日利亚",
    "挪威",
    "阿曼",
    "巴基斯坦",
    "巴拿马",
    "巴布亚新几内亚",
    "巴拉圭",
    "秘鲁",
    "菲律宾",
    "波兰",
    "葡萄牙",
    "卡塔尔",
    "罗马尼亚",
    "俄罗斯",
    "卢旺达",
    "圣基茨和尼维斯",
    "圣卢西亚",
    "圣文森特和格林纳丁斯",
    "萨摩亚",
    "圣马力诺",
    "圣多美和普林西比",
    "沙特阿拉伯",
    "塞内加尔",
    "塞尔维亚",
    "塞舌尔",
    "塞拉利昂",
    "新加坡",
    "斯洛伐克",
    "斯洛文尼亚",
    "所罗门群岛",
    "索马里",
    "南非",
    "韩国",
    "南苏丹",
    "西班牙",
    "斯里兰卡",
    "苏丹",
    "苏里南",
    "斯威士兰",
    "瑞典",
    "瑞士",
    "叙利亚",
    "塔吉克斯坦",
    "坦桑尼亚",
    "泰国",
    "东帝汶",
    "多哥",
    "汤加",
    "特立尼达和多巴哥",
    "突尼斯",
    "土耳其",
    "土库曼斯坦",
    "乌干达",
    "乌克兰",
    "阿拉伯联合酋长国",
    "英国",
    "美国",
    "乌拉圭",
    "乌兹别克斯坦",
    "瓦努阿图",
    "委内瑞拉",
    "越南",
    "也门",
    "赞比亚",
    "津巴布韦",
    "中国台湾",
    "中国香港",
    "中国澳门",
]
