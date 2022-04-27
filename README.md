# OTE-API OntoKB Plugin

An OTE-API Plugin with OTE strategies.

Further reading:

- [OTE-API Core Documentation](https://emmc-asbl.github.io/oteapi-core)
- [OTE-API Services Documentation](https://emmc-asbl.github.io/oteapi-services)

## License and copyright

OTE-API OntoKB Plugin is released under the [MIT license](LICENSE) with copyright &copy; UNIBO.

## Acknowledgment

OTE-API OntoKB Plugin has been created via the [cookiecutter](https://cookiecutter.readthedocs.io/) [template for OTE-API plugins](https://github.com/EMMC-ASBL/oteapi-plugin-template).

OTE-API OntoKB Plugin has been supported by the following projects:

- **OntoTrans** (2020-2024) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 862136.

---

## Usage

The OntoKB Plugin provides three kind of strategies:
* The [sparql_query](#sparql-query) filter strategy
* The [ontokb_access](#ontokb-access) dateresource strategy
* The [ontokb_upload](#ontokb-upload) dateresource strategy

### SparQL query
The sparql query filter strategy allows to provide a SparQL query inside a pipeline. It stores the query and the configuration inside the pipeline during the execution of the GET method, so it need to be placed before any other ontokb_access strategy.

Here the custom configuration:
```python
configuration = {
    "reasoning" : bool  # Enable reasoning during query
}
```

and an example of the strategy created with the otelib library:
```python
sparql_query = client.create_filter(
    filterType="filter/sparql_query",
    query="""PREFIX : <http://emmo.info/domain-mappings#>
            PREFIX app4: <http://semantic-systems.org/ess/ontotrans/app4#>
            PREFIX resin: <http://ontotrans.eu/meta/0.1/Resin#>
                            
            SELECT ?s ?l ?o
            WHERE {
                ?s rdfs:subClassOf ?o .
                ?o rdfs:label "ResinIngredient"@en .
                ?s rdfs:label ?l 
            }""",
    configuration = {
        "reasoning" : True
    }
)
```

### OntoKB access
The OntoKB access plugin provide a read-only access to the databases of your OntoKB instance. It check whether a sparql query is present in the cache and execute it, otherwise it returns all the data contained in the db. All the functionalities are executed through OntoREC.

Here the custom configuration:
```python
configuration = {
    "database": str # The database name 
}
```

and an example of the strategy created with the otelib library:
```python
data_resource = client.create_dataresource(
    accessUrl = "http://host.docker.internal:80",   # The address of your OntoREC instance
    accessService = "datasource/ontokb",
    configuration = {
        "database":"TriplestoreApp3"
    }
)
```

### OntoKB upload
The OntoKB access plugin provide a write-only access to the databases of your OntoKB instance. It allows to add new ontologies to an existing database. The plugin looks for datacache configuration, if it exists the tool will use the content (**rdf ontology**) inside the cache, otherwise it will use the downloadUrl configuration to download the ontology file and add to OntoKB. The download is currently performed with a FileStrategy.
All the functionalities are executed through OntoREC.

Here the custom configuration:
```python
configuration = {
    "database": str,    # The database name
    "filename": str,    # The name of the file to add
    "fileConfig": {
        "downloadUrl": str,    # The URL of the file to download with a FileStrategy
        "mediaType": str,   # The media type of the content
        "configuration":{   # The configuration of the FileStrategy
            "text" : False, 
            "encoding" : "utf-8"
        }
    }
    "datacache_config": DataCacheConfig # the configuration of the cache to use for retrieving the data
}
```

and an example of the strategy created with the otelib library:
```python
uploader = client.create_dataresource(
    accessUrl = "http://host.docker.internal:80",   # The address of your OntoREC instance
    accessService = "datasource/ontokb_upload",
    configuration = {
        "database":"temp",
        "filename":"full_ontology_inferred_remapped.rdf",
        "fileConfig": {
            "downloadUrl":"file:///app/full_ontology_inferred_remapped.rdf",
            "mediaType":"application/json",
            "configuration":{
                "text" : False,
                "encoding" : "utf-8"
            }
        },
    }
)
```