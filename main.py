# -*- coding: utf-8 -*-
# Copyright 2022 WebEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Steamlink Launcher for Kodi
"""

import xbmc
import xbmcaddon
import xbmcvfs
import os.path
import stat
import time

from subprocess import check_output, CalledProcessError


def process_status(process_name):
    try:
        check_output(["pgrep", process_name])
        return True
    except CalledProcessError:
        return False


class KodiAddon(object):
    def __init__(self):
        self._addon = xbmcaddon.Addon()
        self._ADDON_ID = 'plugin.program.retroarch'
        self._path = xbmcvfs.translatePath('special://home/addons/' + self._ADDON_ID)

    def run(self):
        xbmc.executebuiltin('InhibitScreensaver(true)')
        self.create_files()
        check_output(['bash', self._path + '/resources/lib/start.sh'])

        xbmc.executebuiltin('InhibitScreensaver(false)')
        xbmc.executebuiltin('ActivateWindow(home)')

    def create_files(self):
        batch_filename = self._path + '/resources/lib/start.sh'
        if not os.path.isfile(batch_filename):
            with open(batch_filename, 'w') as outfile:
                outfile.write("""#!/bin/bash
            retroarch
            """)
                outfile.close()

            st = os.stat(batch_filename)
            os.chmod(batch_filename, st.st_mode | stat.S_IEXEC)


def main():
    addon = KodiAddon()
    addon.run()


main()
