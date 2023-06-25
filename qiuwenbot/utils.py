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


def get_template_regex(name: str = r"[^{\|#0-9][^{\|#]*?") -> re.Pattern:
    """Get templates regex.

    Parameters
    ----------
    name : str, optional
        Name or regex of the template, by default all templates.

    Returns
    -------
    List[str]
        Templates.
    """
    return re.compile(
        r"""
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
        }}}}
        |
        (?P<unhandled_depth>{{{{\s*[^{{\|#0-9][^{{\|#]*?\s* [^{{]* {{{{ .* }}}})
        """.format(
            name=name
        ),
        re.VERBOSE | re.DOTALL,
    )


def devide_parameters(params: str) -> Dict[str, str]:
    """Devide parameters and remove subtemplate in it.

    Parameters
    ----------
    params : str
        parameters

    Returns
    -------
    Dict[str, str]

    Parameters
    ----------
    """
    if params is None:
        return []
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
