###########################
#### This module manages the counter we should
#### start encrypting from, in case of multiple
#### instances of the server, the counters would be assigned
#### to non-overlapping number ranges e.g. CPU1: 1, CPU2: 50000
###########################


counter = 1


def increment_counter_value():
    global counter
    counter += 1


def get_counter_value():
    global counter
    return counter

def set_counter_value(value):
    global counter
    counter = value