# coding: utf-8

from bson import ObjectId

from django.core.exceptions import ObjectDoesNotExist
from tastypie.bundle import Bundle
from tastypie.resources import Resource


class MongoDBResource(Resource):
    """
    A base resource that allows to make CRUD operations for mongodb.
    """

    def get_object_class(self):
        return self._meta.object_class

    def get_collection(self):
        """
        Encapsulates collection name.
        """
        raise NotImplementedError("You should implement get_collection method.")

    def get_object_list(self, request):
        return self.obj_get_list(request)

    def obj_get_list(self, bundle, **kwargs):
        """
        Maps mongodb documents to resource's object class.
        """

        db = self.get_collection()
        result = []

        self.authorized_read_list(result, bundle)

        for doc in db.find():
            result.append(self.get_object_class()(doc))

        return result

    def obj_get(self, bundle, **kwargs):
        """
        Returns mongodb document from provided id.
        """

        obj = self.get_collection().find_one({
            "_id": ObjectId(kwargs.get("pk"))
        })

        if not obj:
            raise ObjectDoesNotExist

        return self.get_object_class()(obj)

    def obj_create(self, bundle, **kwargs):
        """
        Creates mongodb document from POST data.
        """
        bundle.data.update(kwargs)
        bundle.obj = self.get_collection().insert(bundle.data)
        return bundle

    def obj_update(self, bundle, **kwargs):
        """
        Updates mongodb document.
        """
        self.get_collection().update(
            {"_id": ObjectId(kwargs.get("pk"))},
            {"$set": bundle.data}
        )
        return bundle

    def obj_delete(self, bundle, **kwargs):
        """
        Removes single document from collection
        """
        parameters = {"_id": ObjectId(kwargs.get("pk"))}
        self.get_collection().remove(parameters)

    def obj_delete_list(self, bundle, **kwargs):
        """
        Removes all documents from collection
        """
        self.get_collection().remove()

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object, it returns the extra kwargs needed
        to generate a detail URI.

        By default, it uses the model's ``pk`` in order to create the URI.
        """
        detail_uri_name = getattr(self._meta, 'detail_uri_name', 'pk')
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            if isinstance(bundle_or_obj.obj, ObjectId):
                kwargs[detail_uri_name] = str(bundle_or_obj.obj)
            else:
                kwargs[detail_uri_name] = getattr(bundle_or_obj.obj, detail_uri_name)
        else:
            kwargs[detail_uri_name] = getattr(bundle_or_obj, detail_uri_name)

        return kwargs
