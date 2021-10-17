import sqljin.sjEvent as event

event.subscribe('print', print)
event.trigger('print', 'This is super special')
