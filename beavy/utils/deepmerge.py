
def deepmerge(a, b):
    "merges b into a"
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deepmerge(a[key], b[key])
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
