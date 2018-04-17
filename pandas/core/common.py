def _dict_keys_to_ordered_list(mapping):
    # when pandas drops support for Python < 3.6, this function
    # can be replaced by a simple list(mapping.keys())
    #if PY36 or isinstance(mapping, OrderedDict):
    keys = list(mapping.keys())
    return keys
    #else: