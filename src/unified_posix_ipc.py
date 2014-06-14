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

import os
import posix_ipc # http://semanchuk.com/philip/posix_ipc


SignalError = posix_ipc.SignalError
PermissionsError = posix_ipc.PermissionsError
ExistentialError = posix_ipc.ExistentialError
BusyError = posix_ipc.BusyError

CREAT = posix_ipc.O_CREAT
EXCL = posix_ipc.O_EXCL

def keycat(*keys):
    return ''.join(keys)

def keysep(keys):
    return ['/' + key for key in keys[1:].split('/')]

class Semaphore(posix_ipc.Semaphore):
    def __init__(self, *args, **kwargs):
        posix_ipc.Semaphore.__init__(self, *args, **kwargs)
        self.key = self.name
    def acquire(self, timeout = None, delta = 1):
        have = 0
        try:
            for _ in range(abs(delta)):
                posix_ipc.Semaphore.acquire(self, timeout)
                have += 1
        except Exception as e:
            try:
                self.release(have)
            except:
                pass
            raise e
    def release(self, delta = 1):
        for _ in range(abs(delta)):
            posix_ipc.Semaphore.release(self)
    def P(self, timeout = None, delta = 1):
        self.acquire(timeout, delta)
    def V(self, delta = 1):
        self.release(delta)
    def Z(self, timeout = None):
        if not timeout == 0:
            import sys
            print('Z operation over POSIX semaphore require spinlock', file = sys.stderr)
        if timeout is None:
            while not self.value == 0:
                pass
        elif timeout == 0:
            if not self.value == 0:
                raise BusyError()
        else:
            import time
            end = time.monotonic() + timeout
            while not self.value == 0:
                if time.monotonic() > end:
                    raise BusyError()
    def set_value(self, value):
        n = abs(value) - self.value
        try:
            if n > 0:
                for _ in range(n):
                    self.V()
            elif n < 0:
                for _ in range(-n):
                    self.P(0)
        except BusyError:
            pass
    def remove(self):
        self.unlink()
        self.close()

class SharedMemory(posix_ipc.SharedMemory):
    def __init__(self, *args, **kwargs):
        posix_ipc.SharedMemory.__init__(self, *args, **kwargs)
        self.key = self.name
    def read(self, byte_count = 0, offset = 0):
        rc = []
        byte_count = self.size if byte_count == 0 else byte_count
        byte_count = min(byte_count, self.size - offset)
        os.lseek(self.fd, offset, os.SEEK_SET)
        while len(rc) < byte_count:
            rc += list(os.read(self.fd, byte_count - len(rc)))
        return bytes(rc)
    def write(self, s, offset = 0):
        s = s[:min(len(s), self.size - offset)]
        os.lseek(self.fd, offset, os.SEEK_SET)
        while len(s) > 0:
            s = s[os.write(self.fd, s):]
    def close(self):
        self.close_fd()
    def remove(self):
        self.unlink()
        self.close()

class MessageQueue(posix_ipc.MessageQueue):
    def __init__(self, *args, **kwargs):
        posix_ipc.MessageQueue.__init__(self, *args, **kwargs)
        self.key = self.name
    def remove(self):
        self.unlink()
        self.close()

