# Feature: patients controller — (routing placeholder). Connects: patient_service and router.

from core.request import parse_json_body
from core.responses import send_json, send_404
from services.patient_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_update,
    service_delete,
)


def handle_list(handler):
    """GET /api/patients - Get all patients"""
    try:
        patients = service_get_all()
        return send_json(handler, 200, patients)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_get(handler, patient_id):
    """GET /api/patients/{id} - Get a patient by ID"""
    try:
        patient = service_get_one(patient_id)
        if not patient:
            return send_404(handler)
        return send_json(handler, 200, patient)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_create(handler):
    """POST /api/patients - Create a new patient"""
    try:
        data = parse_json_body(handler)
        if not data:
            return send_json(handler, 400, {"error": "Invalid request body"})
        created = service_create(data)
        return send_json(handler, 201, created)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_update(handler, patient_id):
    """PUT /api/patients/{id} - Update a patient"""
    try:
        data = parse_json_body(handler) or {}
        existing = service_get_one(patient_id)
        if not existing:
            return send_404(handler)
        
        # Merge with existing data to avoid losing fields
        allowed = ["first_name", "last_name", "age", "gender", "phone"]
        merged = {k: data.get(k, existing.get(k)) for k in allowed}
        
        updated = service_update(patient_id, merged)
        if not updated:
            return send_404(handler)
        return send_json(handler, 200, updated)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_delete(handler, patient_id):
    """DELETE /api/patients/{id} - Delete a patient"""
    try:
        deleted = service_delete(patient_id)
        if not deleted:
            return send_404(handler)
        return send_json(handler, 200, deleted)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})
