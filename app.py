from flask import Flask, jsonify, request

app = Flask(__name__)

from products import products

@app.route('/ping', methods=['Get']) #si mo se especifica el methods, toma Get por defecto
def ping():
    return jsonify({ 
        "response": "pong"
    })

@app.route('/products', methods=['GET'])
def getProducts():
   # return jsonify(products)
    return jsonify({
            "products": products,
            "message": "Products List"
        })
#@app.route('/products/:product_name', methods=['GET']) #se puede espesificar asi o como sigue
@app.route('/products/<string:product_name>', methods=['GET']) 
def getProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound)>0):
        return jsonify({"products": productsFound[0]})
    return jsonify({"message": "Products not Found!"})

@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({
        "message": "Product Added Succesfully",
        "products": products
    })

@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]     

    if (len(productsFound)>0):
        productsFound[0]['name']= request.json['name']
        productsFound[0]['price']= request.json['price']
        productsFound[0]['quantity']= request.json['quantity']
        return jsonify({
            "message": "Product Updated",
            "product": productsFound[0]
        })
    return jsonify({"message": "Products not Found!"})

@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]

    if (len(productsFound)>0):
        products.remove(productsFound[0])
        return jsonify({
            "message": "Product Deleted",
            "products": products
        })
    return jsonify({
        "message": "Product not Found!"
    })


if __name__ == '__main__':
    app.run(debug=True, port=4000)