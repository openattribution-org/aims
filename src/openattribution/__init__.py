"""OpenAttribution namespace package."""

# Use pkgutil to support namespace packages across multiple installation paths.
# This allows openattribution.aims and openattribution.telemetry to be installed
# as separate packages but share the openattribution namespace.
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
