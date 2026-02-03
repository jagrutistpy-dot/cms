# Feature: invoices controller — (routing placeholder). Connects: invoice_service and router.

from core.request import parse_json_body
from core.responses import send_json, send_404
from services.invoice_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_update,
    service_delete,
)


def handle_list(handler):
    """GET /api/invoices - Get all invoices"""
    try:
        invoices = service_get_all()
        return send_json(handler, 200, invoices)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_get(handler, invoice_id):
    """GET /api/invoices/{id} - Get an invoice by ID"""
    try:
        invoice = service_get_one(invoice_id)
        if not invoice:
            return send_404(handler)
        return send_json(handler, 200, invoice)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_create(handler):
    """POST /api/invoices - Create a new invoice"""
    try:
        data = parse_json_body(handler)
        if not data:
            return send_json(handler, 400, {"error": "Invalid request body"})
        created = service_create(data)
        return send_json(handler, 201, created)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_update(handler, invoice_id):
    """PUT /api/invoices/{id} - Update an invoice"""
    try:
        data = parse_json_body(handler) or {}
        existing = service_get_one(invoice_id)
        if not existing:
            return send_404(handler)
        
        # Merge with existing data to avoid losing fields
        allowed = ["patient_id", "doctor_id", "amount", "issued_on", "description"]
        merged = {k: data.get(k, existing.get(k)) for k in allowed}
        
        updated = service_update(invoice_id, merged)
        if not updated:
            return send_404(handler)
        return send_json(handler, 200, updated)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_delete(handler, invoice_id):
    """DELETE /api/invoices/{id} - Delete an invoice"""
    try:
        deleted = service_delete(invoice_id)
        if not deleted:
            return send_404(handler)
        return send_json(handler, 200, deleted)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})
