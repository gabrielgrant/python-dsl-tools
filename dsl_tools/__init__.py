
class KWArgAutoSaver(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def make_declarative_metaclass(
    declarations_name, declared_type=None,
    filter_func=None,
    set_declaration_name_callback=None,
    remove_declaration=True,
    #set_declaration_name_method_name=None,
):
    """
    construct a metaclass that allows declarative creation of subclasses
    
    - set_declaration_name_method_name is the name of the method that should
      be called on the declaration to inform it of its declared name
    - filter_func is used to filter the declaration before registering them
    
    set_declaration_name_callback=lambda declaration, name: declaration.name = name
    
    Implementation borrows heavily from django-haystack
    see: https://github.com/toastdriven/django-haystack/blob/master/haystack/indexes.py
    """
    # exactly one of filter_func and declared_type should be defined (XOR)
    # http://stackoverflow.com/questions/432842/how-do-you-get-the-logical-xor-of-two-variables-in-python
    if not (bool(filter_func) ^ bool(declared_type)):  
        print filter_func
        print declared_type
        raise ValueError("Either filter_func or declared_type must be defined")
    
    if not filter_func:
        filter_func = lambda obj: isinstance(obj, declared_type)
    
    class DeclarativeMetaclass(type):
        def __new__(cls, name, bases, attrs):
            attrs[declarations_name] = {}
            
            # Inherit any declarations from parent(s).
            parents = [b for b in bases if isinstance(b, DeclarativeMetaclass)]
            
            for p in parents:
                declarations = getattr(p, declarations_name, None)
                
                if declarations:
                    attrs[declarations_name].update(declarations)
            
            for declared_name, obj in attrs.items():
                if filter_func(obj):
                    if remove_declaration:
                        declaration = attrs.pop(declared_name)
                    else:
                        declaration = attrs[declared_name]
                    if set_declaration_name_callback:
                        # inform the declaration of its name
                        set_declaration_name_callback(declaration, declared_name)
                    # save the declaration
                    attrs[declarations_name][declared_name] = declaration
            
            return super(DeclarativeMetaclass, cls).__new__(cls, name, bases, attrs)
    return DeclarativeMetaclass