from verda._version import __version__
from verda.verda import VerdaClient

import warnings

class _DataCrunchClientAlias:
    def __call__(self, *args, **kwargs):
        warnings.warn(
            "DataCrunchClient is deprecated; use VerdaClient instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return VerdaClient(*args, **kwargs)

# creates a callable that behaves like the class
DataCrunchClient = _DataCrunchClientAlias()
DataCrunchClient.__name__ = "DataCrunchClient"
DataCrunchClient.__doc__ = VerdaClient.__doc__
