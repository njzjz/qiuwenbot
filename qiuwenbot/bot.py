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


def login(user: str, password: str) -> pywikibot.Site:
    """Login to qiuwen.

    Parameters
    ----------
    user
        username of the bot
    password
        password of the bot

    Returns
    -------
    pywikibot.Site
        qiuwen site
    """
    site = pywikibot.Site(
        code="zh",
        fam="qiuwen",
        user=user,
    )
    pywikibot.login.ClientLoginManager(
        site=site, user=user, password=password
    ).login_to_site()
    site.login()
    return site


def get_page(title: str, site: pywikibot.Site):
    """Get the page with the specific title.

    Parameters
    ----------
    title : str
        title of the page
    site : pywikibot.Site
        qiuwen site
    """
    return pywikibot.Page(site, title)
