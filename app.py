# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import signal
import sys
from types import FrameType
import http

from flask import Flask, jsonify, request, abort

from utils.logging import logger
from config import database
from config.database import db

from model import Invoice

app = Flask(__name__)
app = database.init_app(app)


@app.route("/")
def hello() -> str:
    # Use basic logging with custom fields
    logger.info(logField="custom-entry", arbitraryField="custom-entry")

    # https://cloud.google.com/run/docs/logging#correlate-logs
    logger.info("Child logger with trace Id.")

    return "Hello, World!"


@app.route("/invoices", methods=["GET"])
def list_invoices():
    invoices = Invoice.query.all()
    return jsonify([invoice.to_dict() for invoice in invoices]), http.HTTPStatus.OK


@app.route("/invoices", methods=["POST"])
def create_invoice():
    data = request.json
    if not data or not all(k in data for k in ("user_id", "amount")):
        abort(400, description="Missing required fields: user_id, amount")

    new_invoice = Invoice(
        user_id=data["user_id"],
        amount=data["amount"]
    )
    db.session.add(new_invoice)
    db.session.commit()
    return jsonify(new_invoice.to_dict()), http.HTTPStatus.CREATED


@app.route("/invoices/<string:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify(invoice.to_dict()), http.HTTPStatus.OK


@app.route("/invoices/<string:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.json
    if not data:
        abort(400, description="Missing request body")

    if "user_id" in data:
        invoice.user_id = data["user_id"]
    if "amount" in data:
        invoice.amount = data["amount"]

    db.session.commit()
    return jsonify(invoice.to_dict()), http.HTTPStatus.OK


@app.route("/invoices/<string:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return '', http.HTTPStatus.NO_CONTENT


def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")

    from utils.logging import flush

    flush()

    # Safely exit program
    sys.exit(0)


if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)
