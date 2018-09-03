from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from helloflask.auth import login_required
from helloflask.db import get_db
from . import client

bp = Blueprint('product', __name__)


@bp.route('/product')
def index():
    db = get_db()
    products = db.execute(
        'SELECT c.id as client_id, p.id as id, product_name, product_desc, product_price'
        ' FROM product p JOIN client c ON p.client_id = c.id'
    ).fetchall()

    return render_template('product/index.html', products=products)


@bp.route('/createProduct', methods=('GET', 'POST'))
@login_required
def createProduct():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_price = request.form['product_price']
        client_id = request.form['client_id']
        error = None

        if not client_id:
            error = 'client id is required.'
        if not product_name:
            error = 'product name is required.'
        if not product_desc:
            error = 'product phone is required.'
        if not product_price:
            error = 'product email is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (product_name, product_desc, product_price ,client_id)'
                ' VALUES (?, ?, ?,?)',
                (product_name, product_desc, product_price, client_id)
            )
            db.commit()
            return redirect(url_for('product.index'))

    return render_template('product/create.html', clients=client.get_all_clients())


def get_product(id):
    product = get_db().execute(
        'SELECT c.id as client_id,p.id, p.product_name, p.product_desc, p.product_price, p.created FROM product p'
        ' JOIN client c ON p.client_id = c.id'
    ).fetchone()

    if product is None:
        abort(404, "product id {0} doesn't exist.".format(id))

    return product


@bp.route('/<int:id>/updateProduct', methods=('GET', 'POST'))
@login_required
def updateProduct(id):
    product = get_product(id)

    if request.method == 'POST':
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_price = request.form['product_price']
        error = None

        if not product_name:
            error = 'product name is required.'
        if not product_desc:
            error = 'product desc is required.'
        if not product_price:
            error = 'product price is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET product_name = ?, product_desc = ?, product_price = ?'
                ' WHERE id = ?',
                (product_name, product_desc, product_price, id)
            )
            db.commit()
            return redirect(url_for('product.index'))

    return render_template('product/update.html', product=product)


@bp.route('/<int:id>/deleteProduct', methods=('POST',))
@login_required
def deleteProduct(id):
    get_product(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('product.index'))
