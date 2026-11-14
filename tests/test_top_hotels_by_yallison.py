
from helpers import run_cli


def test_top_hotels_are_ranked_descending(tmp_path):
    """O ranking mostra os hotéis de maior valor primeiro, independente da ordem do id e do nome"""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H07", "hotel_name": "Hotel Y", "amount": "220.00"},
            {"reservation_id": "R-2", "hotel_id": "H04", "hotel_name": "Hotel J", "amount": "900.00"},
            {"reservation_id": "R-3", "hotel_id": "H02", "hotel_name": "Hotel F", "amount": "870.00"},
            {"reservation_id": "R-4", "hotel_id": "H10", "hotel_name": "Hotel K", "amount": "100.00"},
        ],
        top=3,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H04", "H02", "H07"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["900.00", "870.00", "220.00"]