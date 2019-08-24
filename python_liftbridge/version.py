import pkg_resources

try:
    __version__ = pkg_resources.get_distribution('python-liftbridge').version
except Exception:
    __version__ = 'unknown'
