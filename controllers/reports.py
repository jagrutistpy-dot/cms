# Feature: reports controller — (routing placeholder). Connects: report_service and router.

from core.responses import send_json
from services.report_service import service_get_enrollment_report
from services.invoice_service import service_get_all as service_get_all_invoices


def handle_enrollment_report(handler):
    """GET /api/reports/enrollments - Get enrollment report (students/courses)"""
    try:
        report = service_get_enrollment_report()
        return send_json(handler, 200, report)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})


def handle_billing_report(handler):
    """GET /api/reports/billing - Get billing report (all invoices)"""
    try:
        invoices = service_get_all_invoices()
        return send_json(handler, 200, invoices)
    except Exception as e:
        return send_json(handler, 500, {"error": str(e)})
