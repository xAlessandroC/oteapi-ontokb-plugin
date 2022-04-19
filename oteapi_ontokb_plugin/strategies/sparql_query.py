"""SPARQL query filter strategy."""
# pylint: disable=no-self-use,unused-argument
from pydantic.dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from pydantic import Field

from oteapi.models import SessionUpdate, AttrDict
from oteapi.models.filterconfig import FilterConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class SessionUpdateSPARQLQueryFilter(SessionUpdate):
    """Return model for `SPARQLQuery`."""

    sparql_query: str = Field(
        ..., description="SPARQL query definition."
    )

    reasoning: bool = Field(
        ...,
        description="Enable reasoning for this specific query"
    )

class SPARQLQueryConfig(AttrDict):
    """Configuration model for SPARQL query data."""

    reasoning: Optional[bool] = Field(
        False,
        description="Enable reasoning for this specific query"
    )

class SPARQLQueryFilterConfig(FilterConfig):
    """SPARQL Query strategy filter config."""

    filterType: str = Field(
        "filter/sparql_query",
        const=True,
        description=FilterConfig.__fields__["filterType"].field_info.description,
    )
    configuration: SPARQLQueryConfig = Field(
        ..., description="SPARQL query filter strategy-specific configuration."
    )


@dataclass
class SPARQLQueryFilter:
    """SPARQL Filter Strategy."""

    filter_config: SPARQLQueryFilterConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy"""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateSPARQLQueryFilter:
        """Execute the strategy.

        This method will be called through the strategy-specific endpoint of the
        OTE-API Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """
        return SessionUpdateSPARQLQueryFilter(sparql_query = self.filter_config.query, reasoning = self.filter_config.configuration.reasoning)