from dataclasses import dataclass

@dataclass
class A:
    x: int

@dataclass
class B:
    y: A

@dataclass
class C:
    z: B

# illegal
try:
    c_thing = C
    c_thing.z.y.x = 0
except AttributeError:
    print("can't do that!")

# equivalent to
try:
    c_thing = {"z": {}}
    c_thing["z"]["y"]["x"] = 0 
except KeyError:
    print("can't do that either!")

# legal
c_thing = C
breakpoint()
c_thing.z = B
c_thing.z.y = A
c_thing.z.y.x = 0

breakpoint()

# also equivalent to
c_thing = {"z": {}}
c_thing["z"]["y"] = {}
c_thing["z"]["y"]["x"] = 0

# equivalent to
c_thing = {"z": {"y": {"x": 0}}}

