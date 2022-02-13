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
from bs4 import BeautifulSoup
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from pywikibot import Site
from typing import Tuple

from .bot import login, get_page
from .qwlogger import qwlogger
from .utils import archieve_page


def get_removed_urls(user: str, site: Site) -> list:
    """Get removed urls from [[User:USER/removed_refs]].

    One keyword per line.

    Parameters
    ----------
    user : str
        username of the bot
    site : pywikibot.Site
        qiuwen site

    Returns
    -------
    list
        list of keywords
    """
    page = get_page("User:%s/removed_refs" % user, site)
    return page.text.strip().split("\n")


def clean_refs(text: str, removed_urls: list, user: str = "") -> Tuple[str, int]:
    """Clean references from the wiki text.

    Parameters
    ----------
    text : str
        original wiki text
    removed_urls : list
        list of removed URLs
    user : str
        username of the bot

    Returns
    -------
    str
        new wiki text
    int
        number of removed references
    """
    bs = BeautifulSoup(text, features='lxml')
    refs = bs.find_all("ref")
    n = 0
    for ref in refs:
        removed = tuple((url in str(ref) for url in removed_urls))
        try:
            ii = removed.index(True)
        except ValueError:
            continue
        else:
            n += 1
            text = text.replace(
                str(ref.encode(formatter=None), 'utf-8'), "<!-- removed_ref site%d by %s -->" % (ii, user))
    return text, n


def logging(site: Site, user: str, title: str, n: int) -> None:
    """Logging the removing operator.
    
    Parameters
    ----------
    site : pywikibot.Site
        qiuwen site
    user : str
        username of the bot
    title : str
        title of the modified page
    n : int
        number of removed references
    """
    page = get_page("User:%s/removed_refs_log" % user, site)
    if len(page.text.split("\n")) > 2000:
        page = archieve_page(page, site)
    page.text += "\n# [[%s]] - removed %d refs - ~~~~~" % (title, n)
    page.save("[[User:Njzjzbot/task0|记录移除参考文献的条目]]")


def main(user: str, password: str, restart: bool=False):
    """Start cleaning references task.
    
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
    removed_urls = get_removed_urls(user, site)
    if restart:
        # read from last page
        logging_page = get_page("User:%s/removed_refs_log" % user, site)
        last_item = logging_page.text.strip().split("\n")[-1]
        title = last_item.split("-")[0].strip()[4:-2]
        qwlogger.info("restart from %s" % title)
        all_pages = site.allpages(start=title)
    else:
        all_pages = site.allpages()
    
    with logging_redirect_tqdm():
        n_removed = tqdm(position=2, desc="Removed refs")
        n_modified = tqdm(position=1, desc="Modified pages")
        for page in tqdm(all_pages, desc="Scanned pages"):
            if page.isRedirectPage():
                continue
            try:
                new_text, n = clean_refs(page.text, removed_urls, user=user)
            except:
                qwlogger.error("%s parsed error!!" % page.title())
                new_text, n = page.text, 0
            if n:
                page.text = new_text
                try:
                    page.save("[[User:Njzjzbot/task0|移除%d个参考文献]]" % n)
                except:
                    pass
                n_removed.update(n)
                n_modified.update(1)
                # log
                logging(site, user, page.title(), n)
