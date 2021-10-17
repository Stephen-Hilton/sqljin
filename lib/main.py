import sys
from .sqljin.sjEvent import *


args = sys.argv
event.trigger('print', args)

event.subscribe('print', print)
event.trigger('print', 'This is super special')

