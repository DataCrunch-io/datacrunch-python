try:
    from importlib.metadata import version
    __version__ = version('datacrunch')
except Exception:
    __version__ = "0.0.0+dev" # fallback for development
