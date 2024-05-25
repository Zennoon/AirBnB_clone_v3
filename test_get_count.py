#!/usr/bin/python3
"""Tests the .get() and .count() methods"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

if storage.count(State) > 0:
    first_state_id = list(storage.all(State).values())[0].id
    print("First State: {}".format(storage.get(State, first_state_id)))

new_state = State(name="California")
new_state.save()

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

if storage.count(State) > 0:
    first_state_id = list(storage.all(State).values())[0].id
    print("First State: {}".format(storage.get(State, first_state_id)))
