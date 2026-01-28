"""Utility functions for the application."""


def stripe_map_execution_status(event_type: str) -> str:
    """Map Stripe event types to execution status."""
    if event_type.endswith(".succeeded") or event_type in {
        "invoice.paid",
    }:
        return "success"

    if event_type.endswith(".failed") or event_type in {
        "invoice.payment_failed",
    }:
        return "failed"

    return "pending"
