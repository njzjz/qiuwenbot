import os

import pytest
import pywikibot
from pywikibot import Page

from qiuwenbot.qwlogger import qwlogger
from qiuwenbot.task.task import Task


class UnitTestTask(Task):
    """A task for unit test.

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
            r"User:%s/unittest_log" % user,
            "单元测试",
        )

    def do(self, page: Page) -> bool:
        """Do the task."""
        page.text = "单元测试，时间戳：%s" % pywikibot.Timestamp.now().isoformat()
        try:
            page.save("njzjz/qiuwenbot: 单元测试", asynchronous=True)
        except (pywikibot.exceptions.Error,):
            qwlogger.exception("Failed to save page %s" % page.title())
            return False
        return True


@pytest.mark.skipif(
    os.environ.get("QIUWENBOT_TEST_USER") is None, reason="No test user."
)
@pytest.mark.skipif(
    os.environ.get("QIUWENBOT_TEST_PASSWORD") is None, reason="No test password."
)
def test_task():
    """Test task."""
    user = os.environ.get("QIUWENBOT_TEST_USER")
    password = os.environ.get("QIUWENBOT_TEST_PASSWORD")
    task = UnitTestTask(
        user=user,
        password=password,
        pages={
            "type": "page",
            "name": "User:%s/unittest" % user,
        },
    )
    task.submit()
