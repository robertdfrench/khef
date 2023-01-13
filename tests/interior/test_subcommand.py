from .. import khef

def test_subcommand_registration():
    @khef.Subcommand
    def long_days_pleasant_nights():
        pass

    assert 'long_days_pleasant_nights' in khef.Subcommand.instances.keys()

def test_subcommand_invocation():
    invoked = []

    @khef.Subcommand
    def long_days_pleasant_nights():
        """This is a mock subcommand"""
        invoked.append("invoked")

    argv = ["long-days-pleasant-nights"]
    khef.Subcommand.dispatch(argv, prog='p', version='v', description='d')
    assert invoked[0] == "invoked"

def test_subcommand_arguments():
    class Nights(khef.Argument):
        pass

    invoked = []

    @khef.Subcommand
    def long_days_pleasant_nights(nights: Nights):
        """This is a mock subcommand"""
        invoked.append(nights)

    argv = ["long-days-pleasant-nights", "two"]
    khef.Subcommand.dispatch(argv, prog='p', version='v', description='d')
    assert invoked[0] == "two"
