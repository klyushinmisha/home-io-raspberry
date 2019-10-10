def to_redis_format(data):
    """Cast bool to string, because
    Redis is not able to work with boolean"""
    for k, v in data.items():
        if type(v) is bool:
            v = str(v).lower()
        data[k] = v
    return data


def to_python_format(data):
    """Cast string to bool, because
    Redis is not able to work with boolean"""
    for k in data.keys():
        v = data[k]
        if v.lower() == 'true' or v.lower() == 'false':
            data[k] = bool(v)
    return data
