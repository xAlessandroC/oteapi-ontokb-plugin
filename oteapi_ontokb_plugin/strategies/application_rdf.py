# pylint: disable=no-self-use,unused-argument
import json
from typing import TYPE_CHECKING, Optional

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.plugins import create_strategy
from pydantic import Field
from pydantic.dataclasses import dataclass

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class RDFConfig(AttrDict):
    """JSON parse-specific Configuration Data Model."""

    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description=(
            "Configurations for the data cache for storing the downloaded file "
            "content."
        ),
    )


class RDFParseConfig(ResourceConfig):
    """File download strategy filter config."""

    mediaType: str = Field(
        "application/rdf",
        const=True,
        description=ResourceConfig.__fields__["mediaType"].field_info.description,
    )
    configuration: RDFConfig = Field(
        RDFConfig(), description="RDF parse strategy-specific configuration."
    )


class SessionUpdateRDFParse(SessionUpdate):
    """Class for returning values from RDF Parse."""

    content: str = Field(..., description="Content of the RDF document.")


@dataclass
class RDFDataParseStrategy:
    """Parse strategy for RDF.
    **Registers strategies**:
    - `("mediaType", "application/RDF")`
    """

    parse_config: RDFParseConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateRDFParse:
        """Parse json."""

        downloader = create_strategy("download", self.parse_config)
        output = downloader.get()
        cache = DataCache(self.parse_config.configuration.datacache_config)
        content = cache.get(output["key"])
        print(type(content))

        # print("[RDF PARSER PLUGIN]: Content is " + content)

        return SessionUpdateRDFParse(content=content)