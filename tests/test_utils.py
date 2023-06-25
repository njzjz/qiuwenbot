import textwrap

from qiuwenbot.utils import devide_parameters, get_cat_regex, get_template_regex


def test_category():
    text = textwrap.dedent(
        """\
        [[Category:abc]]
        [[分類:def]]
        [[分类:ghi]]
        """
    )
    p = get_cat_regex()
    m = p.finditer(text)
    assert [g.group("name") for g in m] == ["abc", "def", "ghi"]


def test_template():
    text = textwrap.dedent(
        """\
        {{abc|def|2=ghi}}
        {{def}}
        """
    )
    p = get_template_regex()
    m = p.finditer(text)
    assert [g.group("name") for g in m] == ["abc", "def"]
    m = p.finditer(text)
    assert [g.group("params") for g in m] == ["def|2=ghi", None]


def test_split_params():
    p = devide_parameters("def|2=ghi{{ssd|1=fd}}")
    assert p == {"1": "def", "2": "ghi"}
