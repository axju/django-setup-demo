from pkg_resources import get_distribution, DistributionNotFound


try:
    __version__ = get_distribution(__name__).version
except BaseException:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound
