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
from pywikibot import Site
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from .bot import login, get_page
from .utils import archieve_page


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
    page = get_page("User:%s/replaced_roc_flags_log" % user, site)
    if len(page.text.split("\n")) > 2000:
        page = archieve_page(page, site)
    page.text += "\n# [[%s]] - replaced %d flags - ~~~~~" % (title, n)
    page.save("[[User:Njzjzbot/task1|记录替换旗帜的条目]]")


def clean_roc(site: Site, user: str):
    """Replace ROC flags with PRC flags.
    
    Parameters
    ----------
    site : pywikibot.Site
        qiuwen site
    user : str
        username of the bot
    """
    roc_template = get_page("Template:ROC", site)

    # compiled res
    re_birth = re.compile(r'Category:(\d+)年出生')
    re_death = re.compile(r'Category:(\d+)年逝世')
    re_found = re.compile(r'Category:(\d+)年(.*)(设立|建立|成立|创建|創建|設立)(.*)')
    re_event = re.compile(r'Category:(\d+)年(台灣)(.*)')

    re_roc = re.compile(r'({{[\s]*ROC[\s]*}})')
    re_nationality = re.compile(r'\|[\s]*(國籍|国籍|nationality)[\s]*=[\s]*({{[\s]*ROC[\s]*}})')
    re_death_place = re.compile(r'\|[\s]*(逝世地點|逝世地点|death_place|place_of_death|resting_place)[\s]*=[\s]*({{[\s]*ROC[\s]*}})')

    comment = "<!-- replaced_flag 0 by %s -->" % user
    replaced_chn = r"{{CHN}}" + comment
    replaced_chn_nationality = r"|\1={{PRC-TWN}}" + comment
    replaced_chn_no_flag = r"|\1=[[中国]]" + comment
    replaced_death_place = r"|\1={{CHN}}" + comment

    with logging_redirect_tqdm():
        n_replaced = tqdm(position=2, desc="Replaced flags")
        n_modified = tqdm(position=1, desc="Modified pages")
        for page in tqdm(roc_template.getReferences(), desc="Scanned pages"):
            reason = None
            replace_all = False
            replace_death = False
            replace_nationality = False
            replace_nationality_no_flag = False
            yy = []
            for cat in page.categories():
                m = re_birth.match(cat.title())
                if m:
                    y = m.group(1)
                    if int(y) > 1949:
                        reason = "新中国成立后出生的人物"
                        replace_all = True
                        replace_nationality = True
                        break
                m = re_death.match(cat.title())
                if m or cat.title() == '在世人物':
                    y = m.group(1)
                    if int(y) > 1949:
                        reason = "在世人物或新中国成立后逝世的人物"
                        replace_death = True
                        replace_nationality_no_flag = True
                        break
                m = re_found.match(cat.title())
                if m:
                    y = m.group(1)
                    yy.append(int(y))
                m = re_event.match(cat.title())
                if m:
                    y = m.group(1)
                    yy.append(int(y))
            if len(yy) and min(yy) > 1949:
                reason = "新中国成立后出现的事物"
                replace_all = True
            if reason is not None:
                n = 0
                if replace_nationality:
                    # nationality
                    try:
                        page.text, n1 = re_nationality.subn(replaced_chn_nationality, page.text)
                    except:
                        continue
                    n += n1
                if replace_nationality_no_flag:
                    # nationality
                    try:
                        page.text, n1 = re_nationality.subn(replaced_chn_no_flag, page.text)
                    except:
                        continue
                    n += n1
                if replace_death:
                    try:
                        page.text, n1 = re_death_place.subn(replaced_death_place, page.text)
                    except:
                        continue
                    n += n1
                if replace_all:
                    try:
                        page.text, n1 = re_roc.subn(replaced_chn, page.text)
                    except:
                        continue
                    n += n1
                if n:
                    try:
                        page.save(("[[User:Njzjzbot/task1|替换%d个非法旗帜]] - " % n) + reason)
                    except:
                        continue
                    logging(site, user, page.title(), n)
                    n_replaced.update(n)
                    n_modified.update(1)


def main(user, password):
    """Replace ROC flags with PRC flags.
    
    Parameters
    ----------
    user : str
        username of the bot
    password : str
        password of the bot
    """
    site = login(user, password)
    clean_roc(site, user)
