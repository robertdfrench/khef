# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .. import khef
import pathlib


def test_version():
    version = khef.Curl.version()
    assert 'curl' in version
    assert len(version.split()) == 2


def test_download():
    absolute_source = pathlib.Path.cwd() / "source.txt"
    with open(absolute_source, "w") as f:
        f.write("source")
    source_url = f"file://{absolute_source}"
    dest = "dest.txt"
    khef.Curl.download(source_url, dest)
    with open(dest, "r") as f:
        assert f.read() == "source"

