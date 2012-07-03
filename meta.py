import inspect

def interface(interface_class):
    class Interface(type):
        def __new__(cls, name, bases, dct):
            for interface_attr, interface_value in interface_class.__dict__.iteritems():
                if not inspect.isfunction(interface_value):
                    continue
                if interface_attr not in dct:
                    raise NotImplementedError('{} is not implemented for {}'.format(interface_attr, name))
                check_signatures(interface_value, dct[interface_attr])
    return Interface

def check_signatures(orig, new):
    if not inspect.isfunction(new):
        raise NotImplementedError('{} should be a function but is a {}'.format(new, type(new)))
    orig_args = inspect.getargspec(orig).args
    new_args = inspect.getargspec(new).args
    if orig_args != new_args:
        raise NotImplementedError('argument diff in {}: {} vs. {}'.format(new, orig_args, new_args))
