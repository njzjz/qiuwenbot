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
from typing import Generator
from pywikibot import Site, Page

from .task import Task
from ..filter.filter import FilterChain, default_filters

class FilterTask(Task):
    """A task to pass filters.
    
    Parameters
    ----------
    site : Site
        Site to operate.
    user : str
        Username.
    password : str
        Password.
    pages : Generator[Page]
        Pages to operate.
    logging_page : str, optional
        Page to log the task, by default None
    summary : str, optional
        Summary of the task, by default emptry string
    """
    def __init__(self,
                 site: Site,
                 user: str,
                 password: str,
                 pages: Generator[Page],
                 logging_page: str = None):
        """Initialize."""
        super().__init__(site, user, password, pages,
                         r"User:%s/filter_log" % user,
                         "综合治理",
                         )
        self.filter = FilterChain(default_filters)

    def do(self, page: Page) -> bool:
        """Do the task."""
        text = page.text
        new_text = self.filter.filter(page.text)
        if new_text == text:
            return False
        page.text = new_text
        page.save(filter.log)
        return True