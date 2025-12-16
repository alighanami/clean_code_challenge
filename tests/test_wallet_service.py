from interns_challenges_number1.wallet_service import get_wallet_status


def test_get_wallet_status_returns_ok():
    result = get_wallet_status()

    assert result["service"] == "wallet"
    assert result["status"] == "ok"
    assert "alive" in result["detail"]
