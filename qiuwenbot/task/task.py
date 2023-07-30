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

from pywikibot import Page, Timestamp
from pywikibot.pagegenerators import PreloadingGenerator
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from qiuwenbot.bot import get_page, login
from qiuwenbot.qwlogger import qwlogger
from qiuwenbot.utils import archieve_page


class Task(metaclass=ABCMeta):
    """A task to be done.

    Parameters
    ----------
    user : str
        Username.
    password : str
        Password.
    pages : dict
        Pages to operate.
    logging_page : str, optional
        Page to log the task, by default None
    summary : str, optional
        Summary of the task, by default emptry string
    """

    def __init__(
        self,
        user: str,
        password: str,
        pages: dict,
        logging_page: str = None,
        summary: str = "",
    ):
        """Initialize."""
        self.site = login(user, password)
        if logging_page is not None:
            self.logging_page = get_page(logging_page, self.site)
        else:
            self.logging_page = None
        if pages["type"] == "all":
            if pages.get("restart", False):
                last_item = self.logging_page.text.strip().split("\n")[-1]
                title = last_item.split("-")[0].strip()[4:-2]
                qwlogger.info("restart from %s" % title)
            else:
                title = ""
            self.pages = self.site.allpages(
                namespace=pages.get("namespace", 0), start=title
            )
        elif pages["type"] == "new":
            start = pages.get("start", None)
            if start is not None:
                start = Timestamp.fromISOformat(start)
            end = pages.get("end", None)
            if end is not None:
                end = Timestamp.fromISOformat(end)
            self.pages = (
                change[0]
                for change in self.site.newpages(
                    returndict=True,
                    namespaces=pages.get("namespace", 0),
                    start=start,
                    end=end,
                )
            )
        elif pages["type"] in ("link", "template"):
            template = get_page(pages["name"], self.site)
            self.pages = template.getReferences(namespaces=pages.get("namespace", None))
        elif pages["type"] == "page":
            self.pages = [get_page(pages["name"], self.site)]
        else:
            raise RuntimeError("Unsupported pages type")
        self.summary = summary

    @abstractmethod
    def do(self, page: Page) -> bool:
        """Do the task."""
        raise NotImplementedError

    def logging(self, title: str) -> None:
        """Log the removing operator.

        Parameters
        ----------
        title : str
            title of the modified page
        """
        if self.logging_page is not None:
            if len(self.logging_page.text.split("\n")) > 2000:
                self.logging_page = archieve_page(self.logging_page, self.site)
            self.logging_page.text += "\n# [[%s]] - ~~~~~" % title
            self.logging_page.save(self.summary, asynchronous=True)

    def submit(self):
        """Submit the task."""
        with logging_redirect_tqdm():
            n_modified = tqdm(position=1, desc="Modified pages")
            for page in tqdm(PreloadingGenerator(self.pages), desc="Scanned pages"):
                if self.do(page):
                    n_modified.update(1)
                    self.logging(page.title())
