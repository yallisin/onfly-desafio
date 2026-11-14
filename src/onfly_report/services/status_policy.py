"""Política de status das reservas."""

from __future__ import annotations


def is_billable(status: str) -> bool:
    """Indica se a reserva entra nos totais financeiros e de noites."""
    """Conferindo se é CONFIRMADO ao invés de != CANCELLED, pois o NO_SHOW também é faturável"""
    return status == "CONFIRMED"