# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import os


# Show that running `khef init` creates a config file in the expected place in
# the user's home directory.
def test_init_creates_config_dir():
    khef.main("init","will.dearborn")
    path = os.path.expanduser("~/.config/nkhef")
    assert os.path.exists(f"{path}/config.json")
