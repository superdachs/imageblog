#!/usr/bin/env python

import argparse
import os
import subprocess
import sys
import re

__doc__ = "blabla"

class Mount():
    def mount(self, args):
        if not os.path.isdir(args.mountpoint):
            raise Exception("ERROR: Mountpoint " + args.mountpoint + " don't exist!")

        try:
            f = open(os.path.join(args.mountpoint, "testfile_nagios.tmp"), 'w')
            f.write('data')
            f.close()
            os.remove(os.path.join(args.mountpoint, "testfile_nagios.tmp"))
        except Exception:
            raise Exception('ERROR: Mountpoint ' + args.mountpoint + " isn't writeable")

        try:
            return getattr(self, "mount_" + args.fstype)(args)
        except Exception:
            raise Exception("ERROR: Could not mount!")

    def umount(self, args):
        cmdline = "umount " + args.mountpoint
        p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(cmdline)
        return p.wait()

    def mount_sshfs(self, args):
        cmdline = "echo '" + args.password + "' | sshfs " + args.user + "@" + args.host + ":" + args.target + " " + args.mountpoint + " -o password_stdin,uid=`id -u nagios`,gid=`id -g nagios`"
        print(cmdline)
        p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.wait()

class Check():
    def check(self, args):
        if args.mountpoint == '':
            raise Exception("ERROR: Command argument missing!")
        try:
            return getattr(self, "check_" + args.command)(args)
        except Exception:
            raise Exception("ERROR: Could not exec command!")


    def check_dirEmptyTrue(self, args):
        if args.cdir == '':
            raise Exception("Check dir argument missing")
        path = os.path.join(args.mountpoint, args.cdir)
        if os.listdir(path) == []:
            print("OK: Directory " + args.cdir + " is empty.")
            sys.exit(0)
        else:
            print("CRITICAL: Directory " + args.cdir + " is not empty.")
            sys.exit(2)

    def check_dirEmptyFalse(self, args):
        if args.cdir == '':
            raise Exception("Check dir argument missing")
        path = os.path.join(args.mountpoint, args.cdir)
        if os.listdir(path) == []:
            print("CRITICAL: Directory " + args.cdir + " is empty.")
            sys.exit(2)
        else:
            print("OK: Directory " + args.cdir + " is not empty.")
            sys.exit(0)

    def check_fileCount(self, args):
       if args.cdir == '':
            raise Exception("Check dir argument missing")
       if args.o == '':
            raise Exception("Additional argument with count missing")
        path = os.path.join(args.mountpoint, args.cdir)
        count = 0
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)):
                count = count + 1
        if count == args.o:
            print("OK: " + count + " files found. Expected " + args.o)
            sys.exit(0)
        else:
            print("CRITICAL: " + count + " files found. Expected " + args.o)
            sys.exit(2)
    
    def check_fileCountMin(self, args):
        if args.cdir == '':
            raise Exception("Check dir argument missing")
        if args.o == '':
            raise Exception("Additional argument with count missing")
        path = os.path.join(args.mountpoint, args.cdir)
        count = 0
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)):
                count = count + 1
        if count >= args.o:
            print("OK: " + count + " files found. Files min " + args.o)
            sys.exit(0)
        else:
            print("CRITICAL: " + count + " files found. Files min " + args.o)
            sys.exit(2)

    def check_fileCountMax(self, args):
       if args.cdir == '':
            raise Exception("Check dir argument missing")
       if args.o == '':
            raise Exception("Additional argument with count missing")
        path = os.path.join(args.mountpoint, args.cdir)
        count = 0
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)):
                count = count + 1
        if count <= args.o:
            print("OK: " + count + " files found. Files max " + args.o)
            sys.exit(0)
        else:
            print("CRITICAL: " + count + " files found. Files max " + args.o)
            sys.exit(2)

    def check_fileSize(self, args):
        if args.cfile == '':
            raise Exception("Check file argument missing")
        if args.o == '':
            raise Exception("Additional argument with count missing")
        path = os.path.join(args.mountpoint, args.cdir)
        path = os.path.join(path, args.cfile)
        size = os.path.getsize(path)
        if size == self.decodeToBytes(o.args):
            print("OK: file " + os.cfile + " is " + self.encodeFromBytes(size) + " expected " + self.encodeFromBytes(self.decodeFromBytes(o.args)))
            sys.exit(0)
        else:
            print("CRITICAL: file " + os.cfile + " is " + self.encodeFromBytes(size) + " expected " + self.encodeFromBytes(self.decodeFromBytes(o.args)))
            sys.exit(2)

    def check_fileSizeMin(self, args):
        if args.cfile == '':
            raise Exception("Check file argument missing")
        if args.o == '':
            raise Exception("Additional argument with count missing")
        path = os.path.join(args.mountpoint, args.cdir)
        path = os.path.join(path, args.cfile)
        size = os.path.getsize(path)
        if size <= self.decodeToBytes(o.args):
            print("OK: file " + os.cfile + " is " + self.encodeFromBytes(size) + " expected " + self.encodeFromBytes(self.decodeFromBytes(o.args)))
            sys.exit(0)
        else:
            print("CRITICAL: file " + os.cfile + " is " + self.encodeFromBytes(size) + " expected " + self.encodeFromBytes(self.decodeFromBytes(o.args)))
            sys.exit(2)

    def check_fileSizeMax(self, args):
        if args.cfile == '':
            raise Exception("Check file argument missing")
        if args.o == '':
            raise Exception("Additional argument with count missing")
        path = os.path.join(args.mountpoint, args.cdir)
        path = os.path.join(path, args.cfile)
        size = os.path.getsize(path)
        if size >= self.decodeToBytes(o.args):
            print("OK: file " + os.cfile + " is " + self.encodeFromBytes(size) + " expected " + self.encodeFromBytes(self.decodeFromBytes(o.args)))
            sys.exit(0)
        else:
            print("CRITICAL: file " + os.cfile + " is " + self.encodeFromBytes(size) + " expected " + self.encodeFromBytes(self.decodeFromBytes(o.args)))
            sys.exit(2)

    def check_shareSpaceFree(self, args):
        path = args.mountpoint
        stat = os.statvfs(path)
        free = stat.f_bsize * stat.f_bavail
        warning = int(decodeToBytes(args.w))
        critical = int(decodeToBytes(args.c))
        if free < warning and free < critical:
            print("OK: free space: " + free)
            sys.exit(0)
        else if free >= warning and free < critical:
            print("WARNING: free space: " + free)
            sys.exit(1)
        else if free >= critical and free >= warning:
            print("CRITICAL: free space: " + free)
            sys.exit(2)
        else:
            print("UNKNOWN ERROR!")
            sys.exit(3)

    def check_shareSpaceUsed(self, args):
        path = args.mountpoint
        stat = os.statvfs(path)
        used = stat.f_bsize * (stat.f_blocks - stat.f_bfree)
        warning = int(decodeToBytes(args.w))
        critical = int(decodeToBytes(args.c))
        if used < warning and used < critical:
            print("OK: used space: " + used)
            sys.exit(0)
        else if used >= warning and used < critical:
            print("WARNING: used space: " + used)
            sys.exit(1)
        else if used >= critical and used >= warning:
            print("CRITICAL: used space: " + used)
            sys.exit(2)
        else:
            print("UNKNOWN ERROR!")
            sys.exit(3)

    def check_fileAgeMin(self, args):
        if args.cfile == '':
            raise Exception("Check file argument missing")

    def timeFromArgument(string):
        


    def decodeToBytes(string):
        val = int(re.sub('[MmGgTtKk][Bb]?', '', string))
        
        fac = re.sub('[0-9]*', '', string)
        fac = fac.upper()
        if fac  == 'KB' or fac == 'K':
            return val * 1024
        else if fac == 'MB' or fac == 'M':
            return val * 1024 *1024
        else if fac == 'GB' or fac == 'G':
            return val * 1024 * 1024 * 1024
        else if fac == 'TB' or fac == 'T':
            return val * 1024 * 1024 * 1024 * 1024
        else if fac == '':
            return val
        else:
            raise Exception("Sizes must be kb, mb, gb, tb or plain bytes")

    def encodeFromBytes(String):
        val = int(string)
        try:
            return str(val / (1024 * 1024 * 1024 * 1024)) + 'TB'
        except:
            pass
        try:
            return str(val / (1024 * 1024 * 1024)) + 'GB'
        except:
            pass
        try:
            return str(val / (1024 * 1024)) + 'MB'
        except:
            pass
        try:
            return str(val / 1024) + 'KB'
        except:
            pass

argp = argparse.ArgumentParser(description=__doc__)
argp.add_argument('-H', '--host', dest='host')
argp.add_argument('-u', '--user', dest='user')
argp.add_argument('-p', '--pass', dest='password')

argp.add_argument('-S', '--sharetype', dest='fstype')
argp.add_argument('-t', '--target', dest='target')
argp.add_argument('-m', '--mountpoint', dest='mountpoint')
argp.add_argument('-C', '--command', dest='command')

argp.add_argument('-d', '--checkdir', dest='cdir')

argp.add_argument('-o', '--additional', dest='o')

args = argp.parse_args()

mnt = Mount()
chk = Check()


mnt.umount(args)
mnt.mount(args)

chk.check(args)

mnt.umount(args)

sys.exit(0)




