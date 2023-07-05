import subprocess as sp


def test_cli():
    """Test qiuwenbot CLI."""
    sp.check_output(["qiuwenbot", "-h"])
    sp.check_output(["qiuwenbot", "submit", "-h"])
