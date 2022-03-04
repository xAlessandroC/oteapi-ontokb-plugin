"""ONTOKB resource strategy class for uploading."""

# pylint: disable=no-self-use,unused-argument
from dataclasses import dataclass
from fastapi import File
from pydantic import Field
from typing import TYPE_CHECKING

from oteapi.plugins import create_strategy

from oteapi.models import SessionUpdate, AttrDict, DataCacheConfig
from typing import Any, Dict, Optional
from oteapi.models.resourceconfig import ResourceConfig
from oteapi.strategies.download.file import FileResourceConfig
from oteapi.datacache import DataCache

import requests

class OntoKBUploadConfig(AttrDict):
    """File-specific Configuration Data Model."""

    database: str = Field(
        ...,
        description=(
            "The database to connect to"
        ),
    )
    filename: str = Field(
        None,
        description=(
            "Name (with .rdf or .ttl extension) of the file to save"
        ),
    )
    fileConfig: Optional[FileResourceConfig] = Field(
        None,
        description=(
            "Configuration for the file strategy"
        ),
    )
    datacache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configurations for the data cache for storing the downloaded file content.",
    )

class OntoKBResourceUploadConfig(ResourceConfig):
    """File download strategy filter config."""

    configuration: OntoKBUploadConfig = Field(
        OntoKBUploadConfig(database="EMMO"), description="OntoKB access strategy-specific configuration."
    )


@dataclass
class OntoKBUploadStrategy:
    """Upload Strategy."""

    resource_config: "OntoKBResourceUploadConfig"

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Initialize strategy."""
        
        # Validation part
        # Check if database actually exists

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

        cache = DataCache(self.resource_config.configuration.datacache_config)

        if cache.config.accessKey and cache.config.accessKey in cache:
            print("[ONTOKB UPLOAD PLUGIN]: Cached data")
            key = cache.config.accessKey
        else:
            print("[ONTOKB UPLOAD PLUGIN]: Downloaded data by means of a filter strategy")
            downloader = create_strategy("download", self.resource_config.configuration.fileConfig)
            output = downloader.get()
            key = output["key"]

        content = cache.get(key) # BinaryData

        url = self.resource_config.accessUrl + "/databases/" + self.resource_config.configuration.database
        response = requests.post(url, files={"ontology":(self.resource_config.configuration.filename, content)})

        # Save result in session
        return SessionUpdate()
