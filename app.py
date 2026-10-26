import json
import os
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_STORE_PATH = Path(os.environ.get("PRODUCT_STORE_PATH", "data/products.json"))


def load_products():
    """Liest die persistent gespeicherten Produkte aus der JSON-Datei."""
    with PRODUCT_STORE_PATH.open(encoding="utf-8") as product_file:
        return json.load(product_file)


def save_products(products):
    """Schreibt Änderungen atomar, damit die Produktdatei nicht beschädigt wird."""
    temporary_path = PRODUCT_STORE_PATH.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as product_file:
        json.dump(products, product_file, ensure_ascii=False, indent=2)
        product_file.write("\n")
    temporary_path.replace(PRODUCT_STORE_PATH)

@app.get("/api/hello")
def hello():
    return jsonify({
        "message": "Hello World from Flask!",
        "status": "ok"
    })


@app.get("/api/products")
def get_products():
    return jsonify(load_products())


@app.post("/api/products")
def create_product():
    """Speichert ein neues Produkt in data/products.json."""
    product = request.get_json(silent=True)
    if not isinstance(product, dict):
        return jsonify({"error": "Es wird ein Produkt als JSON-Objekt erwartet."}), 400

    required_fields = ("name", "price", "description")
    missing_fields = [field for field in required_fields if not product.get(field)]
    if missing_fields:
        return jsonify({"error": "Fehlende Pflichtfelder", "fields": missing_fields}), 400

    try:
        product["price"] = round(float(product["price"]), 2)
    except (TypeError, ValueError):
        return jsonify({"error": "price muss eine Zahl sein."}), 400

    products = load_products()
    product["id"] = max((item["id"] for item in products), default=0) + 1
    products.append(product)
    save_products(products)

    return jsonify(product), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
