"""TOML parser compatibility for Python 3.10 and newer."""

from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        try:
            # Standard Python 3.10 installers normally provide pip and its
            # vendored Tomli parser.
            from pip._vendor import tomli as tomllib
        except ModuleNotFoundError:
            from setuptools._vendor import tomli as tomllib


__all__ = ["tomllib"]
