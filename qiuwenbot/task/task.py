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
from abc import ABCMeta, abstractmethod
from typing import Generator

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from pywikibot import Page

from ..bot import login, get_page
from ..utils import archieve_page


class Task(metaclass=ABCMeta):
    """A task to be done.
    
    Parameters
    ----------
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
                 user: str,
                 password: str,
                 pages: Generator[Page],
                 logging_page: str = None,
                 summary: str = ""):
        """Initialize."""
        self.site = login(user, password)
        self.pages = pages
        if logging_page is not None:
            self.logging_page = get_page(logging_page, self.site)
        else:
            self.logging_page = None
        self.summary = summary

    @abstractmethod
    def do(self, page: Page) -> bool:
        """Do the task."""
        raise NotImplementedError

    def logging(self, title: str) -> None:
        """Logging the removing operator.
        
        Parameters
        ----------
        title : str
            title of the modified page
        """
        if self.logging_page is not None:
            if len(self.logging_page.text.split("\n")) > 2000:
                page = archieve_page(page, self.site)
            page.text += "\n# [[%s]] - ~~~~~" % title
            page.save(self.summary)

    def submit(self):
        """Submit the task."""
        with logging_redirect_tqdm():
            n_modified = tqdm(position=1, desc="Modified pages")
            for page in tqdm(self.pages, desc="Scanned pages"):
                if self.do(page):
                    n_modified.update(1)
                    self.logging(page.title())
