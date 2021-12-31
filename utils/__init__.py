
def jsonify(instance, allow=None, exclude=[]):
    # allow是None，说明所有都输出，exclude有效做排除
    # allow非None，必须是列表等序列，exclude无效
    if allow is not None:
        fn = lambda x: x.name in allow
    else:
        fn = lambda x: x.name not in exclude

    cls = type(instance)
    fields = cls._meta.fields

    return {f.name: getattr(instance, f.name) for f in filter(fn, fields)}
