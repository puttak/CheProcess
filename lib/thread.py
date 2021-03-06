#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2009-2017, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''



###############################################################################
# Library for work with thread in pychemqt for improve UI response
#   - WaitforClick: Thread for draw stream in PFD
#   - Evaluate: Thread to insolate entity calculation from gui, used in streams,
#       equipment, and project
###############################################################################

from time import sleep

from PyQt5.QtCore import QThread, QMutex


class WaitforClick(QThread):
    """Thread used in PFD drawing to specified stream input and output or add
    equipment.
    TODO: Use to customize stream drawing"""
    def __init__(self, num, parent=None):
        super(WaitforClick, self).__init__(parent)
        self.setTerminationEnabled(True)
        self.num = num

    def run(self):
        while True:
            sleep(0.1)
            if len(self.parent().Pos) >= self.num:
                break


class Evaluate(QThread):
    """Thread used to insolate calculation process in entities (stream, project
    and equipment, so gui can response while calculation is in process"""
    def __init__(self, parent=None):
        super(Evaluate, self).__init__(parent)
        self.mutex = QMutex()

    def start(self, entity, kwargs):
        self.entity = entity
        self.kwargs = kwargs
        QThread.start(self)

    def run(self):
        self.mutex.lock()
        self.entity(**self.kwargs)
        self.mutex.unlock()
