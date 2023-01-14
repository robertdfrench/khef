# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef

def test_parse_docstring():
    docstring = "Help Text\nDesc Line 1\nDesc Line 2"
    (help_text, desc_text) = khef.Subcommand.parse_doc(docstring)
    assert help_text == "Help Text"
    assert desc_text == "Desc Line 1\nDesc Line 2"

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
