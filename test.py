import os
import sys
import json
from kova import *

if __name__ == '__main__':
    print "hi"
    kova = Kova()
    response = kova.chat("hello")
    print response
