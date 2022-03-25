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
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from pywikibot import Site

from .bot import login, get_page
from .qwlogger import qwlogger
from .utils import archieve_page


def replace_year(string: str) -> str:
    """Replace ROC year from a string.
    
    Parameters
    ----------
    string : str
        string to be replaced
    
    Returns
    -------
    str
        string that has been replaced
    """
    re_roc_year = re.compile(r'(((\[\[([^\[\]]*\|)?(中(华|華))?民(国|國)\]\])|((中(华|華))?民(国|國)))(\d+|[一二三四五六七八九十]+)年)')
    # group 0 is the entire string, group -1 is the year
    matched = re_roc_year.findall(string)
    for mm in matched:
        try:
            roc_year = int(mm[-1])
        except ValueError:
            roc_year = cn2an.cn2an(mm[-1])
        # 38 - 1949
        if roc_year > 38 and roc_year < 1000:
            ce_year = 1911 + roc_year
            entire_year_str = mm[0]
            ce_year_str = "%d年" % ce_year
            string = string.replace(entire_year_str, ce_year_str)
            # remove duplicate
            # first remove links
            string = string.replace("[[%s]]" % ce_year_str, ce_year_str)
            string = string.replace("%s（%s）" % (ce_year_str, ce_year_str), ce_year_str)
            string = string.replace("%s(%s)" % (ce_year_str, ce_year_str), ce_year_str)
            string = string.replace("%s（%s）" % (ce_year_str, str(ce_year)), ce_year_str)
            string = string.replace("%s(%s)" % (ce_year_str, str(ce_year)), ce_year_str)
    return string


def logging(site: Site, user: str, title: str) -> None:
    """Logging the replacing year.
    
    Parameters
    ----------
    site : pywikibot.Site
        qiuwen site
    user : str
        username of the bot
    title : str
        title of the modified page
    """
    page = get_page("User:%s/replace_year_log" % user, site)
    if len(page.text.split("\n")) > 2000:
        page = archieve_page(page, site)
    page.text += "\n# [[%s]] - ~~~~~" % title
    page.save("[[User:Njzjzbot/task4|机器人：记录替换非法纪年的条目]]")


def main(user: str, password: str, restart: bool=False):
    """Start replacing year.
    
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
        logging_page = get_page("User:%s/replace_year_log" % user, site)
        last_item = logging_page.text.strip().split("\n")[-1]
        title = last_item.split("-")[0].strip()[4:-2]
        qwlogger.info("restart from %s" % title)
        all_pages = site.allpages(start=title)
    else:
        all_pages = site.allpages()
    
    with logging_redirect_tqdm():
        n_modified = tqdm(position=1, desc="Modified pages")
        for page in tqdm(all_pages, desc="Scanned pages"):
            if page.isRedirectPage():
                continue
            try:
                new_text = replace_year(page.text)
            except:
                qwlogger.error("%s parsed error!!" % page.title())
                new_text = page.text
            if new_text != page.text:
                page.text = new_text
                try:
                    page.save("[[User:Njzjzbot/task4|机器人：替换非法纪年]]")
                except:
                    pass
                n_modified.update(1)
                # log
                logging(site, user, page.title())
