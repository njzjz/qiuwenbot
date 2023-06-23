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
"""Check duplicated page with different variants
of Chinese titles, such as zh-cn and zh-hk.
"""
from pywikibot import Page, Site
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from zhconv import convert_for_mw

from .bot import get_page, login
from .qwlogger import qwlogger
from .utils import archieve_page

# variants = ("zh-cn", "zh-tw", "zh-hk")
variants = ("zh-hans", "zh-hant")


def check_page(page: Page, site: Site, user: str):
    """Check if a page has duplicated variants.

    arameters
    ----------
    page: pywikibot.Page
        page to check
    site : pywikibot.Site
        qiuwen site
    user : str
        username of the bot
    """
    title = page.title()
    for variant in variants:
        title_v = convert_for_mw(title, variant)
        page_v = get_page(title_v, site)
        if page_v != page and page_v.exists():
            if not page_v.isRedirectPage():
                if page.text.startswith(
                    "<noinclude>{{delete|"
                ) or page_v.text.startswith("<noinclude>{{delete|"):
                    # has been marked to delete
                    continue
                # duplicated pages A2
                reason = "A2"
                page_v.text = (
                    f"<noinclude>{{{{delete|A2|c1=[[User:Njzjzbot/task2|Njzjzbot]]发现-{{'''{title_v}'''}}-与-{{[[{title}]]}}-仅有简繁差异；请管理员复查页面历史记录，合并差异[[Category:Njzjzbot/A2]]}}}}</noinclude>\n"
                    + page_v.text
                )
            else:
                # duplicated redirects R1
                if (
                    variant in ("zh-cn", "zh-hans")
                    and page_v.getRedirectTarget() == page
                ):
                    # do not process zh-hans redirect, otherwise it is wrong
                    continue
                if (
                    convert_for_mw(title_v, "zh-cn") != convert_for_mw(title, "zh-cn")
                    and page_v.getRedirectTarget() == page
                ):
                    # technical issue
                    continue
                reason = "R1"
                page_v.text = (
                    f"<noinclude>{{{{delete|R1|c1=[[User:Njzjzbot/task2|Njzjzbot]]发现-{{'''{title_v}'''}}-与-{{[[:{title}]]}}-仅有简繁差异[[Category:Njzjzbot/R1]]}}}}</noinclude>\n"
                    + page_v.text
                )
            page_v.save(
                f"[[User:Njzjzbot/task2|标记速删模板]]：[[{title_v}]]与[[{title}]]仅有简繁差异"
            )
            logging(site, user, title, title_v, reason=reason)


def logging(site: Site, user: str, title: str, title_v: str, reason: str = "") -> None:
    """Log.

    Parameters
    ----------
    site : pywikibot.Site
        qiuwen site
    user : str
        username of the bot
    title : str
        title of the scanned page
    title_v : str
        title of the modified page
    reason : str
        reason
    """
    page = get_page("User:%s/check_duplicated_log" % user, site)
    if len(page.text.split("\n")) > 2000:
        page = archieve_page(page, site)
    page.text += f"\n# -{{[[:{title}]]}}- - 删除-{{[[:{title_v}]]}}- - {reason} - ~~~~~"
    page.save("[[User:Njzjzbot/task2|记录标记速删模板的条目]]")


def main(user: str, password: str, restart: bool = False, namespace: int = 0):
    """Start checking duplicated pages.

    Parameters
    ----------
    user : str
        username of the bot
    password : str
        password of the bot
    restart : bool, default=False
        restart from the last modified page (requires logs exsiting)
    namespace : int, default=0
        namespace
    """
    site = login(user, password)
    if restart:
        # read from last page
        logging_page = get_page("User:%s/check_duplicated_log" % user, site)
        last_item = logging_page.text.strip().split("\n")[-1]
        title = last_item.split("-")[0].strip()[7:-4]
        qwlogger.info("restart from %s" % title)
        all_pages = site.allpages(start=title, namespace=namespace)
    else:
        all_pages = site.allpages(namespace=namespace)
    with logging_redirect_tqdm():
        for page in tqdm(all_pages, desc="Scanned pages"):
            if page.isRedirectPage():
                continue
            try:
                check_page(page, site, user)
            except Exception:
                pass
