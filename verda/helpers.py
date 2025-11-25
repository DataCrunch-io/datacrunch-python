import json


def stringify_class_object_properties(class_object: type) -> str:
    """Generates a json string representation of a class object's properties and values.

    :param class_object: An instance of a class
    :type class_object: Type
    :return: _description_
    :rtype: json string representation of a class object's properties and values
    """
    class_properties = {
        property: getattr(class_object, property, '')
        for property in class_object.__dir__()  # noqa: A001
        if property[:1] != '_' and type(getattr(class_object, property, '')).__name__ != 'method'
    }
    return json.dumps(class_properties, indent=2)
