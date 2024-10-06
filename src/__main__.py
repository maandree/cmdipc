#!/usr/bin/env python3
# -*- python -*-
copyright='''
cmdipc — System V and POSIX IPC from the command line
Copyright © 2014  Mattias Andrée (m@maandree.se)

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

import sys

from argparser import ArgParser


parser = ArgParser('System V and POSIX IPC from the command line',
                   '\n'.join(['%s -Q [<options>] [receive]'           % sys.argv[0],
                              '%s -Q [<options>] send [--] <message>' % sys.argv[0],
                              '%s -S [<options>] [p|v|z|read]'        % sys.argv[0],
                              '%s -S [<options>] set <value>'         % sys.argv[0],
                              '%s -M [<options>] [read]'              % sys.argv[0],
                              '%s -M [<options>] write [--] <data>'   % sys.argv[0],
                              '%s -X [<options>] [enter|leave]'       % sys.argv[0],
                              '%s -C [<options>] [enter|leave|wait]'  % sys.argv[0],
                              '%s -C [<options>] notify [all]'        % sys.argv[0],
                              '%s -C [<options>] broadcast'           % sys.argv[0],
                              '%s -B [<options>] <threshold> [enter]' % sys.argv[0],
                              '%s -B [<options>] --remove'            % sys.argv[0],
                              '%s -L [<options>] [shared [un]lock]'   % sys.argv[0],
                              '%s -L [<options>] exclusive [un]lock'  % sys.argv[0],
                              '%s -R [<options>] [--] [<message>]'    % sys.argv[0],
                              '%s --ftok <path> <id>'                 % sys.argv[0]]),
                   None, None, True, ArgParser.standard_abbreviations())


parser.add_argumentless(['-h', '-?', '--help'],  0,          'Prints this help message and exits')
parser.add_argumented  (['-k', '--key'],         0, 'KEY',   'The key (SysV) or name (POSIX) of the item')
parser.add_argumented  (['-m', '--mode'],        0, 'OCTAL', 'The mode for the item')
parser.add_argumented  (['-s', '--size'],        0, 'SIZE',  'Maximum size for messages')
parser.add_argumented  (['-z', '--spool'],       0, 'SIZE',  'Maximum number of messages')
parser.add_argumented  (['-t', '--type'],        0, 'TYPE',  'Message type')
parser.add_argumented  (['-p', '--priority'],    0, 'PRIO',  'Message priority')
parser.add_argumented  (['-d', '--delta'],       0, 'DELTA', 'Semaphore value increment')
parser.add_argumented  (['-i', '--initial'],     0, 'VALUE', 'Initial semaphore value')
parser.add_argumented  (['-b', '--timeout'],     0, 'SECS',  'Semaphore V/Z timeout, in seconds')
parser.add_argumented  (['-l', '--length'],      0, 'LEN',   'Shared memory read length')
parser.add_argumented  (['-o', '--offset'],      0, 'OFF',   'Shared memory read/write offset')
parser.add_argumentless(['-r', '--remove'],      0,          'Remove unit')
parser.add_argumentless(['-n', '--nonblocking'], 0,          'Do not block, exit with 2 if busy')
parser.add_argumentless(['-c', '--create'],      0,          'Create item')
parser.add_argumentless(['-x', '--exclusive'],   0,          'Create exclusive item')
parser.add_argumentless(['-f', '--ftok'],        0,          'Create unit ID, possibly non-unique')
parser.add_argumentless(['-P', '--posix'],       0,          'Use POSIX IPC rather than System V IPC')
parser.add_argumentless(['-Q', '--mqueue'],      0,          'Use message queue')
parser.add_argumentless(['-S', '--semaphore'],   0,          'Use semaphore')
parser.add_argumentless(['-M', '--shm'],         0,          'Use shared memory')
parser.add_argumentless(['-X', '--mutex'],       0,          'Use mutex (1 semaphore)')
parser.add_argumentless(['-C', '--condition'],   0,          'Use condition (3 semaphores)')
parser.add_argumentless(['-B', '--barrier'],     0,          'Use barrier (2 semaphores; -P: +1 semaphore)')
parser.add_argumentless(['-L', '--shared-lock'], 0,          'Use shared lock (3 semaphores)')
parser.add_argumentless(['-R', '--rendezvous'],  0,          'Use rendezvous (2 semaphores, 1 mqueue; -P: +1 semaphore)')


parser.parse()
parser.support_alternatives()

if parser.opts['--help'] is not None:
    parser.help()
    sys.exit(0)


if parser.opts['--posix'] is not None:
    import unified_posix_ipc as ipc
    use_posix = True
else:
    import unified_sysv_ipc as ipc
    use_posix = False


try:
    if (not use_posix) and (parser.opts['--ftok'] is not None) and (len(parser.files) == 2):
        print(ipc.ftok(parser.files[0], int(parser.files[1]), silence_warning = True))
    
    elif parser.opts['--mqueue'] is not None:
        key, flags, mode, spool, size, type, timeout = None, 0, 0o600, 10, 8192, None, None
        if not use_posix:
            spool, size = 1, 2048
        if parser.opts['--nonblocking'] is not None:  timeout = 0
        if parser.opts['--key']         is not None:  key     = ipc.keysep(parser.opts['--key'][0])[0]
        if parser.opts['--create']      is not None:  flags   = ipc.CREAT
        if parser.opts['--exclusive']   is not None:  flags   = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']        is not None:  mode    = int(parser.opts['--mode'][0], 8)
        if parser.opts['--size']        is not None:  size    = int(parser.opts['--size'][0])
        if parser.opts['--spool']       is not None:  spool   = int(parser.opts['--spool'][0])
        if parser.opts['--type']        is not None:  type    = int(parser.opts['--type'][0])
        if parser.opts['--priority']    is not None:  type    = int(parser.opts['--priority'][0])
        if parser.opts['--timeout']     is not None:  timeout = float(parser.opts['--timeout'][0])
        q = ipc.MessageQueue(key, flags, mode, spool, size)
        if key is None:
            print('key: %s' % ipc.keycat(q.key))
        nocmd = False
        if (len(parser.files) > 1) and (parser.files[0] == 'send'):
            if type is None:
                type = 0 if use_posix else 1
            q.send(' '.join(parser.files[1:]).encode('utf-8'), timeout, type)
        elif (len(parser.files) == 1) and (parser.files[0] == 'receive'):
            if type is None:
                type = 0
            (message, type) = q.receive(timeout) if use_posix else q.receive(timeout, type)
            print(('priority: %i' if use_posix else 'type: %i') % type)
            print('length: %i' % len(message))
            sys.stdout.buffer.write(message)
            sys.stdout.buffer.write(b'\n')
            sys.stdout.buffer.flush()
        elif key is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            q.remove()
        elif nocmd:
            q.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    elif parser.opts['--semaphore'] is not None:
        key, flags, mode, initial, timeout, delta = None, 0, 0o600, 0, None, 1
        if parser.opts['--nonblocking'] is not None:  timeout = 0
        if parser.opts['--key']         is not None:  key     = ipc.keysep(parser.opts['--key'][0])[0]
        if parser.opts['--create']      is not None:  flags   = ipc.CREAT
        if parser.opts['--exclusive']   is not None:  flags   = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']        is not None:  mode    = int(parser.opts['--mode'][0], 8)
        if parser.opts['--initial']     is not None:  initial = int(parser.opts['--initial'][0])
        if parser.opts['--timeout']     is not None:  timeout = float(parser.opts['--timeout'][0])
        if parser.opts['--delta']       is not None:  delta   = int(parser.opts['--delta'][0])
        s = ipc.Semaphore(key, flags, mode, initial)
        if key is None:
            print('key: %s' % ipc.keycat(s.key))
        nocmd = False
        if   (len(parser.files) == 1) and (parser.files[0] == 'p'):     s.P(timeout, delta)
        elif (len(parser.files) == 1) and (parser.files[0] == 'v'):     s.V(delta)
        elif (len(parser.files) == 1) and (parser.files[0] == 'z'):     s.Z(timeout)
        elif (len(parser.files) == 1) and (parser.files[0] == 'read'):  print('%i' % s.value)
        elif (len(parser.files) == 2) and (parser.files[0] == 'set'):   s.set_value(int(parser.files[1]))
        elif key is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            s.remove()
        elif nocmd:
            s.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    elif parser.opts['--shm'] is not None:
        key, flags, mode, size, length, offset = None, 0, 0o600, None, 0, 0
        if parser.opts['--key']       is not None:  key    = ipc.keysep(parser.opts['--key'][0])[0]
        if parser.opts['--create']    is not None:  flags  = ipc.CREAT
        if parser.opts['--exclusive'] is not None:  flags  = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']      is not None:  mode   = int(parser.opts['--mode'][0], 8)
        if parser.opts['--size']      is not None:  size   = int(parser.opts['--size'][0])
        if parser.opts['--length']    is not None:  length = int(parser.opts['--length'][0])
        if parser.opts['--offset']    is not None:  offset = int(parser.opts['--offset'][0])
        if size is None:
            m = ipc.SharedMemory(key, flags, mode)
        else:
            m = ipc.SharedMemory(key, flags, mode, size)
        if key is None:
            print('key: %s' % ipc.keycat(m.key))
        nocmd = False
        if (len(parser.files) > 1) and (parser.files[0] == 'write'):
            m.write(' '.join(parser.files[1:]).encode('utf-8'), offset)
        elif (len(parser.files) == 1) and (parser.files[0] == 'read'):
            sys.stdout.buffer.write(m.read(length, offset))
            sys.stdout.buffer.write(b'\n')
            sys.stdout.buffer.flush()
        elif key is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            m.remove()
        elif nocmd:
            m.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    elif parser.opts['--mutex'] is not None:
        key, flags, mode, timeout = None, 0, 0o600, None
        if parser.opts['--nonblocking'] is not None:  timeout = 0
        if parser.opts['--key']         is not None:  key     = ipc.keysep(parser.opts['--key'][0])[0]
        if parser.opts['--create']      is not None:  flags   = ipc.CREAT
        if parser.opts['--exclusive']   is not None:  flags   = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']        is not None:  mode    = int(parser.opts['--mode'][0], 8)
        if parser.opts['--timeout']     is not None:  timeout = float(parser.opts['--timeout'][0])
        s = ipc.Semaphore(key, flags, mode, 1)
        if key is None:
            print('key: %s' % ipc.keycat(s.key))
        nocmd = False
        if   (len(parser.files) == 1) and (parser.files[0] == 'enter'):  s.P(timeout)
        elif (len(parser.files) == 1) and (parser.files[0] == 'leave'):  s.V()
        elif key is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            s.remove()
        elif nocmd:
            s.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    elif parser.opts['--condition'] is not None:
        key, flags, mode, timeout = [None, None, None], 0, 0o600, None
        if parser.opts['--nonblocking'] is not None:  timeout = 0
        if parser.opts['--key']         is not None:  key     = ipc.keysep(parser.opts['--key'][0])
        if parser.opts['--create']      is not None:  flags   = ipc.CREAT
        if parser.opts['--exclusive']   is not None:  flags   = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']        is not None:  mode    = int(parser.opts['--mode'][0], 8)
        if parser.opts['--timeout']     is not None:  timeout = float(parser.opts['--timeout'][0])
        s = ipc.Semaphore(key[0], flags, mode, 1)
        c = ipc.Semaphore(key[1], flags, mode, 0)
        q = ipc.Semaphore(key[2], flags, mode, 0)
        if key[0] is None:
            print('key: %s' % ipc.keycat(s.key, c.key, q.key))
        nocmd = False
        if len(parser.files) == 1:
            if   parser.files[0] == 'enter':      s.P(timeout)
            elif parser.files[0] == 'leave':      s.V()
            elif parser.files[0] == 'wait':       s.V() ; c.V() ; q.P(timeout) ; c.P(timeout) ; s.P(timeout)
            elif parser.files[0] == 'notify':     q.V()
            elif parser.files[0] == 'broadcast':
                for _ in range(c.value):
                    q.V()
            elif key[0] is not None:
                nocmd = True
        elif (len(parser.files) == 2) and (parser.files[0] == 'notify') and (parser.files[1] == 'all'):
            for _ in range(max(c.value, 1)):
                q.V()
        elif key[0] is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            s.remove()
            c.remove()
            q.remove()
        elif nocmd:
            s.close()
            c.close()
            q.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    elif parser.opts['--barrier'] is not None:
        key, flags, mode, timeout = [None, None, None], 0, 0o600, None
        if parser.opts['--nonblocking'] is not None:  timeout = 0
        if parser.opts['--key']         is not None:  key     = ipc.keysep(parser.opts['--key'][0])
        if parser.opts['--create']      is not None:  flags   = ipc.CREAT
        if parser.opts['--exclusive']   is not None:  flags   = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']        is not None:  mode    = int(parser.opts['--mode'][0], 8)
        if parser.opts['--timeout']     is not None:  timeout = float(parser.opts['--timeout'][0])
        if len(parser.files) == 0:
            threshold = 1
            if parser.opts['--remove'] is None:
                print('Invalid command given', file = sys.stderr)
                sys.exit(1)
        else:
            threshold = int(parser.files[0])
        if not use_posix:
            s = ipc.Semaphore(key[0], flags, mode, threshold)
            m = ipc.Semaphore(key[1], flags, mode, 1)
            c = ipc.Semaphore(key[2], flags, mode, 0)
            if key[0] is None:
                print('key: %s' % ipc.keycat(s.key, m.key, c.key))
        else:
            x = ipc.Semaphore(key[0], flags, mode, 1)
            c = ipc.Semaphore(key[1], flags, mode, 0)
            q = ipc.Semaphore(key[2], flags, mode, 0)
            if key[0] is None:
                print('key: %s' % ipc.keycat(x.key, c.key, q.key))
        nocmd = False
        if (len(parser.files) == 2) and (parser.files[1] == 'enter'):
            if not use_posix:
                s.P(timeout)
                s.Z(timeout)
                m.P()
                c.V()
                if c.value == threshold:
                    s.set_value(threshold)
                    c.set_value(0)
                m.V()
            else:
                x.P(timeout)
                c.V()
                if c.value == threshold:
                    q.V(threshold - 1)
                    c.set_value(0)
                    x.V()
                else:
                    x.V()
                    q.P(timeout)
        elif key[0] is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            if not use_posix:
                s.remove()
                m.remove()
            else:
                x.remove()
                c.remove()
                q.remove()
        elif nocmd:
            if not use_posix:
                s.close()
                m.close()
            else:
                x.close()
                c.close()
                q.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    elif parser.opts['--shared-lock'] is not None:
        key, flags, mode, timeout = [None, None, None], 0, 0o600, None
        if parser.opts['--nonblocking'] is not None:  timeout = 0
        if parser.opts['--key']         is not None:  key     = ipc.keysep(parser.opts['--key'][0])
        if parser.opts['--create']      is not None:  flags   = ipc.CREAT
        if parser.opts['--exclusive']   is not None:  flags   = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']        is not None:  mode    = int(parser.opts['--mode'][0], 8)
        if parser.opts['--timeout']     is not None:  timeout = float(parser.opts['--timeout'][0])
        x = ipc.Semaphore(key[0], flags, mode, 1)
        s = ipc.Semaphore(key[1], flags, mode, 0)
        m = ipc.Semaphore(key[2], flags, mode, 1)
        if key[0] is None:
            print('key: %s' % ipc.keycat(x.key, s.key, m.key))
        nocmd = False
        verb = ' '.join(parser.files)
        if verb == 'shared lock':
            m.P(timeout)
            if s.value == 0:
                x.P(timeout)
            s.V()
            m.V()
        elif verb == 'exclusive lock':
            x.P(timeout)
        elif verb == 'shared unlock':
            m.P(timeout)
            s.P(timeout)
            if s.value == 0:
                x.V()
            m.V()
        elif verb == 'exclusive unlock':
            x.V()
        elif key[0] is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            x.remove()
            s.remove()
            m.remove()
        elif nocmd:
            x.close()
            s.close()
            m.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    elif parser.opts['--rendezvous'] is not None:
        key, flags, mode, spool, size, timeout = [None, None, None], 0, 0o600, 2, 8192, None
        if use_posix:
            spool, size = 1, 2048
            key = [None] * 4
        if parser.opts['--nonblocking'] is not None:  timeout = 0
        if parser.opts['--key']         is not None:  key     = ipc.keysep(parser.opts['--key'][0])
        if parser.opts['--create']      is not None:  flags   = ipc.CREAT
        if parser.opts['--exclusive']   is not None:  flags   = ipc.CREAT | ipc.EXCL
        if parser.opts['--mode']        is not None:  mode    = int(parser.opts['--mode'][0], 8)
        if parser.opts['--spool']       is not None:  spool   = int(parser.opts['--spool'][0])
        if parser.opts['--size']        is not None:  size    = int(parser.opts['--size'][0])
        if parser.opts['--timeout']     is not None:  timeout = float(parser.opts['--timeout'][0])
        m = ipc.Semaphore(key[0], flags, mode, 1)
        i = ipc.Semaphore(key[1], flags, mode, 0)
        if use_posix:
            p = ipc.Semaphore(key[2], flags, mode, 0)
        q = ipc.MessageQueue(key[3 if use_posix else 2], flags, mode, spool, size)
        if key[0] is None:
            if use_posix:
                print('key: %s' % ipc.keycat(m.key, i.key, p.key, q.key))
            else:
                print('key: %s' % ipc.keycat(m.key, i.key, q.key))
        nocmd = False
        if len(parser.files) > 0:
            send_message = ' '.join(parser.files).encode('utf-8')
            m.P(timeout)
            if i.value == 0:
                i.V()
                m.V()
                if not use_posix:
                    q.send(send_message, timeout, 1)
                    (recv_message, _type) = q.receive(timeout, 2)
                else:
                    q.send(send_message, timeout)
                    p.P()
                    (recv_message, _prio) = q.receive(timeout)
            else:
                i.P(timeout)
                m.V()
                if not use_posix:
                    (recv_message, _type) = q.receive(timeout, 1)
                    q.send(send_message, timeout, 2)
                else:
                    (recv_message, _prio) = q.receive(timeout)
                    p.V()
                    q.send(send_message, timeout)
            print('length: %i' % len(recv_message))
            sys.stdout.buffer.write(recv_message)
            sys.stdout.buffer.write(b'\n')
            sys.stdout.buffer.flush()
        elif key[0] is not None:
            nocmd = True
        if parser.opts['--remove'] is not None:
            m.remove()
            i.remove()
            if use_posix:
                p.remove()
            q.remove()
        elif nocmd:
            m.close()
            i.close()
            if use_posix:
                p.close()
            q.close()
            print('Invalid command given', file = sys.stderr)
            sys.exit(1)
    
    else:
        print('No command given', file = sys.stderr)
        sys.exit(1)

except ipc.SignalError:       sys.exit(5)
except ipc.PermissionsError:  sys.exit(4)
except ipc.ExistentialError:  sys.exit(3)
except ipc.BusyError:         sys.exit(2)
except:                       sys.exit(1)

