# Building a Flask Project for JSON Data Ingestion into Elasticsearch and API Development for Retrieval
---This project aims to develop a Flask-based application to efficiently ingest JSON records into Elasticsearch while also constructing APIs to facilitate seamless data retrieval.
Leveraging Flask, a micro web framework in Python, in conjunction with Elasticsearch, a powerful distributed search and analytics engine, enables the creation of an efficient data pipeline and user-friendly interfaces.

# Ingesting of Json data
----json file containing documents are ingested using bulk operation(from elasticsearch.helpers import bulk) using POST method.
----Raw json data is also ingested.

# retrieving of data
------data is retreived by using GET method by writing the specific query for required the document to retreive
-----elastissearch.search() function is used to retreive the data.

# Updating the data 
-------data is updated by writing the update_by_query() function using POST method
-------sample query
                      {
  "script": {
    "source": "ctx._source.feild_to_update='value';",
    "lang": "painless"
  },
  "query": {
    "match": {"feild":"value"}
  }
}

-- "lang": "painless" is a parameter used in scripts to specify the scripting language being used. 
Painless is a scripting language developed by Elasticsearch for tasks like custom scoring, filtering, and document transformations


# Deleting of data 
------delete_by_query() function is used in deleting the specific required data
------DELETE method is used

