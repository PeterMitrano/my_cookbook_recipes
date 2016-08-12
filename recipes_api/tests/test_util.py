from nose.plugins.attrib import attr

def wip(f):
    return attr('wip')(f)

