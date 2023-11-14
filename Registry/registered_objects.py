from registry import RegistryBase
import uuid

class BaseRegisteredClass(metaclass=RegistryBase):
    pass

class ExtendedRegisteredClass(BaseRegisteredClass):
    in_msg = None
    out_msg = None
    
    def __init__(self, *args, **kwargs):
        self.uuid = uuid.uuid1()
        if "in_msg" in kwargs:
            self.in_msg = kwargs["in_msg"]
        if "out_msg" in kwargs:
            self.out_msg = kwargs["out_msg"]

        BaseRegisteredClass.register_init(self)

class OtherExtendedRegisteredClass(BaseRegisteredClass):
    in_msg = None
    out_msg = None
    def __init__(self, *args, **kwargs):
        self.uuid = uuid.uuid1()
        if "in_msg" in kwargs:
            self.in_msg = kwargs["in_msg"]
        if "out_msg" in kwargs:
            self.out_msg = kwargs["out_msg"]

        BaseRegisteredClass.register_init(self)

if __name__ == "__main__":
    thing_cls = RegistryBase.REGISTRY["ExtendedRegisteredClass"]
    thing_obj = thing_cls(out_msg="hello from extended registered thing!")
    breakpoint()