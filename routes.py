from flask import render_template, request, abort, Blueprint, redirect

import api
from models.models import Product

base_bp = Blueprint('base', __name__)

product_object = api.SensorModelView()


@base_bp.route("/", methods=["GET"])
def redirect():
    return render_template("product/get.html")


@base_bp.route("/product", methods=["GET"])
def redirect_to():
    return render_template("product/get.html")


@base_bp.route("/product/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template('create.html')
    elif request.method == "POST":
        Product.load_from_dict(request.values)
        return redirect()
    else:
        return abort(404)


@base_bp.route("/product/edit/<obj_id>", methods=["GET", "PUT"])
def sensor_edit(obj_id):
    if request.method == "GET":
        return render_template('edit.html', obj=product_object.retrieve(obj_id))
    elif request.method == "PUT":
        product_object.update(obj_id, request)
        return redirect()
    else:
        return abort(404)


@base_bp.route("/product/delete/<obj_id>", methods=["DELETE"])
def sensor_delete(obj_id):
    return product_object.delete(obj_id)
