# Copyright 2022 Alethea Katherine Flowers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from pathlib import Path

import nox

nox.options.error_on_external_run = True


def nox_env_dir(session: nox.Session) -> str:
    return Path(
        session.run("python", "-c", "import sys; print(sys.executable)", silent=True)
    ).parts[-3]


@nox.session(python="3.10")
def a(session):
    print(session.name)


@nox.session(venv="a")
def b(session):
    print(session.name)
    assert nox_env_dir(session) == "a"


@nox.session(requires=["a"])
def c(session):
    print(session.name)
    assert nox_env_dir(session) == session.name


@nox.session(venv="a")
def d(session):
    session.install("nox")


@nox.session(python="3.10", venv_backend="conda")
def e(session):
    print(session.name)


@nox.session(venv="e")
def f(session):
    session.conda_install("numpy")


@nox.session(python=["3.9", "3.10"])
def g(session):
    print(session.name)


@nox.session(python="3.10", venv="g-{python}")
def h(session):
    print(session.name)
    assert nox_env_dir(session) == "g-3-10"


@nox.session(python=["3.9", "3.10"], venv="g-{python}")
def i(session):
    print(session.name)
    if session.python == "3.9":
        assert nox_env_dir(session) == "g-3-9"
    elif session.python == "3.10":
        assert nox_env_dir(session) == "g-3-10"
    else:
        msg = "Unexpected branch."
        raise RuntimeError(msg)


@nox.session(venv="g")
def j(session):
    print(session.name)


@nox.session(venv="does_not_exist")
def k(session):
    print(session.name)


@nox.session(python=None)
def m(session):
    print(session.name)


@nox.session(venv="m")
def n(session):
    print(session.name)
