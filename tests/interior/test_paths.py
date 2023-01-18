# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef


# Show that we get the default value of Config Home when no XDG_CONFIG_HOME
# value is set (when the value of that variable is `None`).
def test_config_home_none():
    assert str(khef.config_home(None)).endswith("/.config")


# Show that we get the default value of Config Home when the XDG_CONFIG_HOME
# value is set to something other than the default.
def test_config_home_some():
    assert str(khef.config_home("~/.altconfig")).endswith("/.altconfig")
