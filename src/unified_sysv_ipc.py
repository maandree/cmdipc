# -*- python -*-
'''
cmdipc — System V and POSIX IPC from the command line
Copyright © 2014  Mattias Andrée (maandree@member.fsf.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sysv_ipc # http://semanchuk.com/philip/sysv_ipc


ftok = sysv_ipc.ftok

PermissionsError = sysv_ipc.PermissionsError
ExistentialError = sysv_ipc.ExistentialError
BusyError = sysv_ipc.BusyError
class SignalError(Exception):
    def __init__(self, *argv, **kwargs):
        Exception.__init__(self, *argv, **kwargs)

CREAT = sysv_ipc.IPC_CREAT
EXCL = sysv_ipc.IPC_EXCL

def keycat(*keys):
    return '.'.join([str(key) for key in keys])

def keysep(keys):
    return [int(key) for key in keys.split('.')]

class Semaphore(sysv_ipc.Semaphore):
    def __init__(self, *args, **kwargs):
        sysv_ipc.Semaphore.__init__(self, *args, **kwargs)
    def set_value(self, value):
        self.value = value
    def close(self):
        pass

class SharedMemory(sysv_ipc.SharedMemory):
    def __init__(self, *args, **kwargs):
        sysv_ipc.SharedMemory.__init__(self, *args, **kwargs)
    def close(self):
        pass

class MessageQueue(sysv_ipc.MessageQueue):
    def __init__(self, key, flags = 0, mode = 0o600, max_messages = 1, max_message_size = 2048):
        sysv_ipc.MessageQueue.__init__(self, key, flags, mode, max_messages * max_message_size)
        self.send_ = sysv_ipc.MessageQueue.send
        self.recv_ = sysv_ipc.MessageQueue.receive
    def send(self, message, timeout = None, type = 1):
        self.send_(self, message, (timeout is None) or (timeout != 0), type)
    def receive(self, timeout = None, type = 1):
        return self.recv_(self, (timeout is None) or (timeout != 0), type)
    def close(self):
        pass

