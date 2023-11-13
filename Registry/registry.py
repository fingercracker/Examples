class RegistryBase(type):

    REGISTRY = {}
    REGISTRY_INIT = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls
    
    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)
    
    @classmethod
    def register_init(cls, obj, *args, **kwargs):
        if type(obj).__name__ not in cls.get_registry():
            raise Exception(f"Tried to register object with name {type(obj).__name__} but that class is not in the registry...")
        # reg_cls_inst = reg_cls(args, kwargs)
        cls.REGISTRY_INIT[obj.uuid] = obj

