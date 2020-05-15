from flask import Flask, jsonify

from conf.db_conf import session, conn_str
from models.models import Product, ProductType
from routes import base_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn_str
app.register_blueprint(base_bp)


@app.route("/products", methods=["GET"])
def get_sensors():
    products = session.query(Product).all()
    products_transformed = []
    for p in products:
        p_type = session.query(ProductType).filter_by(id=p.type_id).first()

        product = {
            'id': p.id,
            'product_name': p.product_name,
            'product_type': p_type.product_type,
            'price': p.price,
            'rating': p.rating,
        }
        products_transformed.append(product)
    return jsonify({'data': products_transformed})


if __name__ == "__main__":
    app.run(debug=True)
