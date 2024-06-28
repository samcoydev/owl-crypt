role_registry = {}


# TODO - Create a base Registry object and make the registries use that

def clear_registry():
    """
    Clear the Role Registry
    :return: None
    """
    role_registry.clear()


def register_role(role_class):
    """
    Register a Role class into the registry.
    :param role_class: The class of the Role to register.
    :return: None
    """
    name = role_class.name
    if name in role_registry:
        raise KeyError(f'Role with name "{name}" already exists')
    role_registry[name] = role_class
