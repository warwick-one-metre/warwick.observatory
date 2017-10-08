#!/usr/bin/env python3
#
# This file is part of warwick.observatory.
#
# warwick.observatory is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# warwick.observatory is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with warwick.observatory.  If not, see <http://www.gnu.org/licenses/>.

"""
Directory of Pyro daemons
"""

# pylint: disable=too-few-public-methods

import datetime
import Pyro4

class PyroDaemon(object):
    """Encodes a reference to a remote Pyro4 daemon"""
    def __init__(self, name, host, port, default_timeout):
        self.name = name
        self.host = host
        self.port = port
        self.default_timeout = default_timeout
        self.uri = 'PYRO:' + name + '@' + host + ':' + str(port)

    def connect(self, timeout=None):
        """Returns a Pyro4 proxy to the remote daemon"""
        proxy = Pyro4.Proxy('PYRO:' + self.name + '@' + self.host + ':' + str(self.port))

        # pylint: disable=protected-access
        if timeout is None:
            proxy._pyroTimeout = self.default_timeout
        elif timeout > 0:
            proxy._pyroTimeout = timeout
        # pylint: enable=protected-access

        return proxy

    def launch(self, daemon):
        """Launches a daemon with the given server object"""
        Pyro4.config.DETAILED_TRACEBACK = True
        Pyro4.config.REQUIRE_EXPOSE = True

        pyro = Pyro4.Daemon(host=self.host, port=self.port)
        uri = pyro.register(daemon, objectId=self.name)

        print('{} MESSAGE: Starting daemon {}'.format(datetime.datetime.utcnow(), uri))
        pyro.requestLoop()
        print('{} MESSAGE: Exiting daemon {}'.format(datetime.datetime.utcnow(), uri))

# pylint: disable=invalid-name
observatory_log = PyroDaemon('observatory_log_daemon', '10.2.6.201', 9016, 5)
observatory_network_ping = PyroDaemon('observatory_netping_daemon', '10.2.6.201', 9012, 5)

onemetre_operations = PyroDaemon('operations_daemon', '10.2.6.202', 9015, 5)
onemetre_environment = PyroDaemon('environment_daemon', '10.2.6.202', 9002, 5)

onemetre_vaisala = PyroDaemon('onemetre_vaisala_daemon', '10.2.6.202', 9001, 5)
onemetre_roomalert = PyroDaemon('onemetre_roomalert_daemon', '10.2.6.202', 9008, 5)
onemetre_network_ping = PyroDaemon('onemetre_netping_daemon', '10.2.6.202', 9012, 5)
onemetre_power = PyroDaemon('onemetre_power_daemon', '10.2.6.202', 9009, 5)
onemetre_rain = PyroDaemon('onemetre_rain_daemon', '10.2.6.202', 9017, 5)

superwasp_log = PyroDaemon('superwasp_daemon', '10.2.6.201', 9007, 5)
tng_log = PyroDaemon('tng_daemon', '10.2.6.201', 9011, 5)

onemetre_dome = PyroDaemon('dome_daemon', '10.2.6.202', 9004, 5)

onemetre_telescope = PyroDaemon('telescope_daemon', '10.2.6.203', 9003, 5)
onemetre_tcs_diskspace = PyroDaemon('onemetre_diskspace_daemon', '10.2.6.203', 9008, 5)
onemetre_blue_camera = PyroDaemon('blue_camera_daemon', '10.2.6.203', 9011, 5)
onemetre_red_camera = PyroDaemon('red_camera_daemon', '10.2.6.203', 9010, 5)
onemetre_pipeline = PyroDaemon('pipeline_daemon', '10.2.6.203', 9012, 5)

nites_roomalert = PyroDaemon('nites_roomalert_daemon', '10.2.6.181', 9008, 5)
nites_dome = PyroDaemon('nites_dome_daemon', '10.2.6.181', 9009, 5)

goto_roomalert = PyroDaemon('goto_roomalert_daemon', '10.2.6.201', 9020, 5)
goto_ups = PyroDaemon('goto_ups_daemon', '10.2.6.201', 9021, 5)

# pylint: enable=invalid-name