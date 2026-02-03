# Feature: doctors controller — (routing placeholder). Connects: doctor_service and router.

from core.request import parse_json_body
from core.responses import send_json, send_404
from services.doctor_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_update,
    service_delete,
)


def handle_list(handler):
    """GET /api/doctors - Get all doctors"""
    try:
        doctors = service_get_all()
        return send_json(handler, 200, doctors)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_get(handler, doctor_id):
    """GET /api/doctors/{id} - Get a doctor by ID"""
    try:
        doctor = service_get_one(doctor_id)
        if not doctor:
            return send_404(handler)
        return send_json(handler, 200, doctor)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_create(handler):
    """POST /api/doctors - Create a new doctor"""
    try:
        data = parse_json_body(handler)
        if not data:
            return send_json(handler, 400, {"error": "Invalid request body"})
        created = service_create(data)
        return send_json(handler, 201, created)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_update(handler, doctor_id):
    """PUT /api/doctors/{id} - Update a doctor"""
    try:
        data = parse_json_body(handler) or {}
        existing = service_get_one(doctor_id)
        if not existing:
            return send_404(handler)
        
        # Merge with existing data to avoid losing fields
        allowed = ["name", "specialization", "phone", "email"]
        merged = {k: data.get(k, existing.get(k)) for k in allowed}
        
        updated = service_update(doctor_id, merged)
        if not updated:
            return send_404(handler)
        return send_json(handler, 200, updated)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_delete(handler, doctor_id):
    """DELETE /api/doctors/{id} - Delete a doctor"""
    try:
        deleted = service_delete(doctor_id)
        if not deleted:
            return send_404(handler)
        return send_json(handler, 200, deleted)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})
