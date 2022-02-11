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
"""This module is aimmed to check duplicated page with different variants 
of Chinese titles, such as zh-cn and zh-hk."""
from zhconv import convert_for_mw
from pywikibot import Site, Page
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from .qwlogger import qwlogger
from .bot import login, get_page
from .utils import archieve_page

#variants = ("zh-cn", "zh-tw", "zh-hk")
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
                if page.text.startswith("{{delete|") or page_v.text.startswith("{{delete|"):
                    # has been marked to delete
                    continue
                # duplicated pages A2
                page_v.text = "{{delete|A2|c1=[[User:Njzjzbot/task2|Njzjzbot]]发现-{'''%s'''}-与-{[[%s]]}-仅有简繁差异；请管理员复查页面历史记录，合并差异[[Category:Njzjzbot/A2]]}}\n" % (title_v, title) + page_v.text
            else:
                # duplicated redirects R1
                if variant in ('zh-cn', 'zh-hans') and page_v.getRedirectTarget() == page:
                    # do not process zh-hans redirect, otherwise it is wrong
                    continue
                if convert_for_mw(title_v, 'zh-cn') != convert_for_mw(title, 'zh-cn') and page_v.getRedirectTarget() == page:
                    # technical issue
                    continue
                page_v.text = "{{delete|R1|c1=[[User:Njzjzbot/task2|Njzjzbot]]发现-{'''%s'''}-与-{[[%s]]}-仅有简繁差异[[Category:Njzjzbot/R1]]}}\n" % (title_v, title) + page_v.text
            page_v.save("[[User:Njzjzbot/task2|标记速删模板]]：[[%s]]与[[%s]]仅有简繁差异" % (title_v, title))
            logging(site, user, title, title_v)


def logging(site: Site, user: str, title: str, title_v: str) -> None:
    """Logging.
    
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
    """
    page = get_page("User:%s/check_duplicated_log" % user, site)
    if len(page.text.split("\n")) > 2000:
        page = archieve_page(page, site)
    page.text += "\n# [[%s]] - 删除[[%s]] - ~~~~~" % (title, title_v)
    page.save("[[User:Njzjzbot/task2|记录标记速删模板的条目]]")


def main(user: str, password: str, restart: bool=False):
    """Start checking duplicated pages.
    
    Parameters
    ----------
    user : str
        username of the bot
    password : str
        password of the bot
    restart : bool, default=False
        restart from the last modified page (requires logs exsiting)
    """
    site = login(user, password)
    if restart:
        # read from last page
        logging_page = get_page("User:%s/check_duplicated_log" % user, site)
        last_item = logging_page.text.strip().split("\n")[-1]
        title = last_item.split("-")[0].strip()[4:-2]
        qwlogger.info("restart from %s" % title)
        all_pages = site.allpages(start=title)
    else:
        all_pages = site.allpages()
    with logging_redirect_tqdm():
        for page in tqdm(all_pages, desc="Scanned pages"):
            if page.isRedirectPage():
                continue
            try:
                check_page(page, site, user)
            except KeyboardInterrupt:
                raise
            except:
                pass
