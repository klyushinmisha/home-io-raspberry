def to_redis_format(self, data):
    """Cast bool to string, because
    Redis is not able to work with boolean"""
    for k, v in data:
        if type(v) is bool:
            v = str(v).lower()
        data[k] = v


def to_python_format(self, data):
    """Cast string to bool, because
    Redis is not able to work with boolean"""
    for k in data.keys():
        v = data[k]
        if v.lower() == 'true' or v.lower() == 'false':
            data[k] = bool(v)
    return data
