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
import pywikibot
from pywikibot import Page, Site
from zhconv import convert_for_mw

from qiuwenbot.bot import get_page
from qiuwenbot.qwlogger import qwlogger
from qiuwenbot.task.task import Task

# variants = ("zh-cn", "zh-tw", "zh-hk")
variants = ("zh-hans", "zh-hant")


def check_page(page: Page, site: Site):
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
                page_v.text = (
                    f"<noinclude>{{{{delete|R1|c1=[[User:Njzjzbot/task2|Njzjzbot]]发现-{{'''{title_v}'''}}-与-{{[[:{title}]]}}-仅有简繁差异[[Category:Njzjzbot/R1]]}}}}</noinclude>\n"
                    + page_v.text
                )
            page_v.save(
                f"[[User:Njzjzbot/task2|标记速删模板]]：[[{title_v}]]与[[{title}]]仅有简繁差异",
                asynchronous=True,
            )


class CheckDuplicatedPageTask(Task):
    """A task to check duplicated pages.

    Parameters
    ----------
    user : str
        Username.
    password : str
        Password.
    pages : str
        Pages to operate.
    """

    def __init__(
        self,
        user: str,
        password: str,
        pages: dict,
    ):
        """Initialize."""
        super().__init__(
            user,
            password,
            pages,
            r"User:%s/check_duplicated_log" % user,
            "检查重复页面",
        )

    def do(self, page: Page) -> bool:
        """Do the task."""
        if page.isRedirectPage():
            return False
        try:
            check_page(page, self.site)
        except pywikibot.exceptions.Error:
            qwlogger.exception("Failed to save page %s" % page.title())
            return False
        return True
