# Feature: billing controller — (routing placeholder). Connects: billing_service and router.

from core.request import parse_json_body
from core.responses import send_json, send_404
from services.billing_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_update,
    service_delete,
)


def handle_list(handler):
    """GET /api/billing - Get all billing records"""
    try:
        billing_records = service_get_all()
        return send_json(handler, 200, billing_records)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_get(handler, billing_id):
    """GET /api/billing/{id} - Get a billing record by ID"""
    try:
        billing = service_get_one(billing_id)
        if not billing:
            return send_404(handler)
        return send_json(handler, 200, billing)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_create(handler):
    """POST /api/billing - Create a new billing record"""
    try:
        data = parse_json_body(handler)
        if not data:
            return send_json(handler, 400, {"error": "Invalid request body"})
        created = service_create(data)
        return send_json(handler, 201, created)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_update(handler, billing_id):
    """PUT /api/billing/{id} - Update a billing record"""
    try:
        data = parse_json_body(handler) or {}
        existing = service_get_one(billing_id)
        if not existing:
            return send_404(handler)
        
        # Merge with existing data to avoid losing fields
        allowed = ["patient_id", "doctor_id", "amount", "issued_on", "description"]
        merged = {k: data.get(k, existing.get(k)) for k in allowed}
        
        updated = service_update(billing_id, merged)
        if not updated:
            return send_404(handler)
        return send_json(handler, 200, updated)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_delete(handler, billing_id):
    """DELETE /api/billing/{id} - Delete a billing record"""
    try:
        deleted = service_delete(billing_id)
        if not deleted:
            return send_404(handler)
        return send_json(handler, 200, deleted)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})
