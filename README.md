MongoDB Resource for Tastypie
=============================

Allows you to create delicious APIs for MongoDB.

Settings
--------

    MONGODB_HOST = None
    MONGODB_PORT = None
    MONGODB_DATABASE = "database_name"

    # optional:
    MONGODB_USERNAME = None
    MONGODB_PASSWORD = None

Example of Usage
----------------

    from tastypie import fields
    from tastypie.authorization import Authorization

    from tastypie_mongodb.resources import MongoDBResource, Document

    class DocumentResource(MongoDBResource):

        id = fields.CharField(attribute="_id")
        title = fields.CharField(attribute="title", null=True)
        entities = fields.ListField(attribute="entities", null=True)

        class Meta:
            resource_name = "documents"
            list_allowed_methods = ["delete", "get", "post"]
            authorization = Authorization()
            object_class = Document
            collection = "documents" # collection name

Contributors
------------

 - Ferrix Hovi (<https://github.com/ferrix>)
 - Alper Kanat (<https://github.com/tunix>)


