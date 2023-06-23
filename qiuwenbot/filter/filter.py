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
from abc import ABCMeta, abstractmethod
from typing import List, Union


class Filter(metaclass=ABCMeta):
    """Filter texts."""

    @abstractmethod
    def filter(self, text: str) -> str:
        """Filter text.

        Parameters
        ----------
        text : str
            Text to filter.

        Returns
        -------
        str
            Filtered text.
        """

    @property
    def log(self) -> Union[str, None]:
        """Log of the filter.

        Returns
        -------
        str
            Log of the filter.
        """


class TextReplaceFilter(Filter):
    """Filter to replace texts.

    Parameters
    ----------
    pattern : str
        Pattern to replace.
    repl : str
        Replacement.
    """

    def __init__(self, pattern: str, repl: str) -> None:
        super().__init__()
        self.prog = re.compile(pattern)
        self.repl = repl

    def filter(self, text: str) -> str:
        """Filter text.

        Parameters
        ----------
        text : str
            Text to filter.

        Returns
        -------
        str
            Filtered text.
        """
        return self.prog.sub(self.repl, text)

    @property
    def log(self) -> str:
        """Log of the filter.

        Returns
        -------
        str
            Log of the filter.
        """
        return f"替换{self.prog.pattern}为{self.repl}"


class FilterChain(Filter):
    """Filter chain.

    Parameters
    ----------
    filters : list of Filter
        Filters to apply.
    """

    def __init__(self, filters: List[Filter]) -> None:
        super().__init__()
        self.filters = [filter() for filter in filters]
        self.active_filters = []

    def filter(self, text: str) -> str:
        """Filter text.

        Parameters
        ----------
        text : str
            Text to filter.

        Returns
        -------
        str
            Filtered text.
        """
        active_filters = []
        for filter in self.filters:
            old_text = text
            text = filter.filter(text)
            if text != old_text:
                active_filters.append(filter)
        self.active_filters = active_filters
        return text

    @property
    def log(self) -> str:
        """Log of the filter.

        Returns
        -------
        str
            Log of the filter.
        """
        logs = []
        for filter in self.active_filters:
            if filter.log is not None:
                logs.append(filter.log)
        return "综合治理：" + "；".join(logs)


default_filters = []


def register_filter(cls: Filter) -> Filter:
    """Return a decorator to register filter.

    The filter should not have any parameters in its constructor.

    Parameters
    ----------
    cls : Filter
        Filter to register.

    Returns
    -------
    Filter
        Registered filter.

    Examples
    --------
    >>> @register_filter()
    ... class Filter1(Filter):
    ...     pass
    """
    default_filters.append(cls)
    return cls
