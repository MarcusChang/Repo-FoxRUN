#!/usr/bin/python

import vcsjob
import sys

from ave.broker import Broker
from ave.broker.exceptions import Busy
from ave.workspace import Workspace


def main():
    prf = vcsjob.get_profiles()
    b = Broker()
    i = 0
    while True:
        try:
            workspace, handset = b.get(*prf)
        except Busy, e:
            break
        i += 1
    print "wokspace number is %d" % i

if __name__ == '__main__':
    main()
