import os
import sys
import json
from kova import *

if __name__ == '__main__':
    kova = Kova()
    while(1):
        message = raw_input('User: ')
        response = kova.chat(message)
        print 'Kova: ' + response
