"""ONTOKB resource strategy class."""
# pylint: disable=no-self-use,unused-argument
from typing import TYPE_CHECKING

from oteapi.models import AttrDict, ResourceConfig, SessionUpdate
from pydantic import Field
from pydantic.dataclasses import dataclass

import requests

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


class OntoKBConfig(AttrDict):
    """File-specific Configuration Data Model."""

    database: str = Field(
        ...,
        description=(
            "The database to connect to"
        ),
    )

class OntoKBResourceConfig(ResourceConfig):
    """File download strategy filter config."""

    configuration: OntoKBConfig = Field(
        OntoKBConfig(database="EMMO"), description="OntoKB access strategy-specific configuration."
    )

class SessionUpdateOntoKBResource(SessionUpdate):
    """Return model for `OntoKB resource strategy`."""

    ontokb_data: dict = Field(
        {}, description="data retrieved from database"
    )

@dataclass
class OntoKBResourceStrategy:
    """Resource Strategy."""

    resource_config: OntoKBResourceConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""
        
        # Validation part
        # Check if database actually exists

        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateOntoKBResource:
        """Execute the strategy.

        This method will be called through the strategy-specific endpoint of the
        OTE-API Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """
        print("[ONTOKB PLUGIN]: Session " + str(session))

        result = {}
        if "sparql_query" in session and session["sparql_query"] != "":
            # SPARQL query defined
            print("[ONTOKB PLUGIN]: Getting query data")
            # reasoning = session["reasoning"] if "reasoning" in session else False
            url = self.resource_config.accessUrl + "/databases/" + self.resource_config.configuration.database + "/query"
        else:
            # SPARQL query doesn't exists
            print("[ONTOKB PLUGIN]: Getting all the data")
            url = self.resource_config.accessUrl + "/databases/" + self.resource_config.configuration.database
            response = requests.get(url)

        result = response.json()

        # Save result in session
        return SessionUpdateOntoKBResource(ontokb_data = result)
