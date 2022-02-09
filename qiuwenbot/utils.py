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
import pywikibot
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
