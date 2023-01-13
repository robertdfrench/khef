from .. import khef


# Show that main is intact and can respond to arguments.
def test_main(capsys):
    khef.main(["--version"])
    assert capsys.readouterr().out.rstrip() == "--version"
