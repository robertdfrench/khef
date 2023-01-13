from .. import khef


# Argv reflects what is passed to it
def test_reflect_arguments(capsys):
    khef.main(["hello", "world"])
    assert capsys.readouterr().out.rstrip() == "hello world"
