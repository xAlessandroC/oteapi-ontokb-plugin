"""SPARQL query filter strategy."""

# pylint: disable=no-self-use,unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from pydantic import BaseModel, Field

from oteapi.models import SessionUpdate

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models.filterconfig import FilterConfig

class SessionUpdateSPARQLQueryFilter(SessionUpdate):
    """Return model for `SPARQLQuery`."""

    sparql_query: str = Field(
        ..., description="sparql query definition."
    )


@dataclass
class SPARQLQueryFilter:
    """SPARQL Filter Strategy."""

    filter_config: "FilterConfig"

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Initialize strategy"""

        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute the strategy.
        This method will be called through the strategy-specific endpoint of the
        OTE-API Services.
        Parameters:
            session: A session-specific dictionary context.
        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.
        """
        return SessionUpdateSPARQLQueryFilter(sparql_query = self.filter_config.query)