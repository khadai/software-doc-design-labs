import json
from models.models import Product
from flask import Response, abort, Blueprint


class BaseView(object):
    __model_class__ = None
    __includes__ = None
    __blueprint__ = None
    __prefix__ = None

    def __init__(self):
        if self.__prefix__ is not None:
            self.__blueprint__ = Blueprint(self.__prefix__, __name__,
                                           url_prefix="/{prefix}".format(prefix=self.__prefix__))

    def get(self):
        return [i.serialize() for i in self.__model_class__.query.all()]

    def post(self, info):
        error = self.check_fields(self.__model_class__.required_fields_list(), info)

        if len(error) > 0:
            return json.dumps(error), 400
        else:
            self.__model_class__.load_from_dict(info.values)
            return Response("created", status=201)

    def retrieve(self, obj_id):
        obj = self.__model_class__.query.get(obj_id)
        if obj:
            return obj.serialize(includes=self.__includes__)
        else:
            return abort(400)

    def update(self, obj_id, info):
        self.__model_class__.query.get(obj_id).edit(info.values)
        return Response("updated", 200)

    def delete(self, obj_id):
        self.__model_class__.query.get(obj_id).remove()
        return Response("deleted", 200)

    @staticmethod
    def check_fields(fields, request):
        error = []
        for field in fields:
            if field not in request.values:
                error.append({"key": field, "message": "Value can not be empty"})
            elif request.values[field] is None or not request.values[field].strip():
                error.append({"key": field, "message": "Value can not be empty"})

        return error


class SensorModelView(BaseView):
    __model_class__ = Product
    __prefix__ = "product"
