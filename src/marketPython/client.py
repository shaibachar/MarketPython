from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from helloflask.auth import login_required
from helloflask.db import get_db

bp = Blueprint('client', __name__)


@bp.route('/client')
def index():
    clients = get_all_clients()
    return render_template('client/index.html', clients=clients)

def get_all_clients():
    db = get_db()
    clients = db.execute(
        'SELECT id, client_name, client_phone, client_email, created'
        ' FROM client c'
        ' ORDER BY created DESC'
    ).fetchall()

    return clients

@bp.route('/createClient', methods=('GET', 'POST'))
@login_required
def createClient():
    if request.method == 'POST':
        client_name = request.form['client_name']
        client_phone = request.form['client_phone']
        client_email = request.form['client_email']
        error = None

        if not client_name:
            error = 'Client name is required.'
        if not client_phone:
            error = 'Client phone is required.'
        if not client_email:
            error = 'Client email is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO client (client_name, client_phone, client_email)'
                ' VALUES (?, ?, ?)',
                (client_name, client_phone, client_email)
            )
            db.commit()
            return redirect(url_for('client.index'))

    return render_template('client/create.html')


def get_client(id):
    client = get_db().execute(
        'SELECT c.id, c.client_name, c.client_phone, c.client_email, c.created FROM client c'
    ).fetchone()

    if client is None:
        abort(404, "Client id {0} doesn't exist.".format(id))

    return client


@bp.route('/<int:id>/updateClient', methods=('GET', 'POST'))
@login_required
def updateClient(id):
    client = get_client(id)

    if request.method == 'POST':
        client_name = request.form['client_name']
        client_phone = request.form['client_phone']
        client_email = request.form['client_email']
        error = None

        if not client_name:
            error = 'Client name is required.'
        if not client_phone:
            error = 'Client phone is required.'
        if not client_email:
            error = 'Client email is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE client SET client_name = ?, client_phone = ?, client_email = ?'
                ' WHERE id = ?',
                (client_name, client_phone, client_email, id)
            )
            db.commit()
            return redirect(url_for('client.index'))

    return render_template('client/update.html', client=client)


@bp.route('/<int:id>/deleteClient', methods=('POST',))
@login_required
def deleteClient(id):
    get_client(id)
    db = get_db()
    db.execute('DELETE FROM client WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('client.index'))
