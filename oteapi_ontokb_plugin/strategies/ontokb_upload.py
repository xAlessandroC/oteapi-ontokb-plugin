"""ONTOKB resource strategy class for uploading."""
# pylint: disable=no-self-use,unused-argument
from typing import TYPE_CHECKING, Optional

import requests
from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig, SessionUpdate
from oteapi.plugins import create_strategy
from oteapi.strategies.download.file import FileResourceConfig
from pydantic import Field
from pydantic.dataclasses import dataclass

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class OntoKBUploadConfig(AttrDict):
    """File-specific Configuration Data Model."""

    database: str = Field(
        ...,
        description=("The database to connect to"),
    )
    filename: str = Field(
        None,
        description=("Name (with .rdf or .ttl extension) of the file to save"),
    )
    fileConfig: Optional[FileResourceConfig] = Field(
        None,
        description=("Configuration for the file strategy"),
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description=(
            "Configurations for the data cache for storing the downloaded file "
            "content."
        ),
    )


class OntoKBResourceUploadConfig(ResourceConfig):
    """File download strategy filter config."""

    configuration: OntoKBUploadConfig = Field(
        OntoKBUploadConfig(database="EMMO"),
        description="OntoKB access strategy-specific configuration.",
    )


@dataclass
class OntoKBUploadStrategy:
    """Upload Strategy."""

    resource_config: OntoKBResourceUploadConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""

        # Validation part
        # Check if database actually exists

        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Execute the strategy.

        This method will be called through the strategy-specific endpoint of the
        OTE-API Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """

        cache = DataCache(self.resource_config.configuration.datacache_config)

        if cache.config.accessKey and cache.config.accessKey in cache:
            print("[ONTOKB UPLOAD PLUGIN]: Cached data")
            key = cache.config.accessKey
        elif "key" in session:
            print("[ONTOKB UPLOAD PLUGIN]: Found file strategy in pipeline")
            key = session["key"]
        else:
            print(
                "[ONTOKB UPLOAD PLUGIN]: Downloaded data by means of a filter strategy"
            )
            downloader = create_strategy(
                "download", self.resource_config.configuration.fileConfig
            )
            output = downloader.get()
            key = output["key"]

        content = cache.get(key)  # BinaryData

        url = (
            self.resource_config.accessUrl
            + "/databases/"
            + self.resource_config.configuration.database
        )
        response = requests.post(
            url,
            files={"ontology": (self.resource_config.configuration.filename, content)},
        )

        if response.status_code/100 != 2 :
            raise Exception("Error during ontorec upload")

        # Save result in session
        return SessionUpdate()
