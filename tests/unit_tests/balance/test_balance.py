import responses # https://github.com/getsentry/responses

from datacrunch.balance.balance import BalanceService, Balance


def test_balance(http_client):
    # arrange - add response mock
    responses.add(
        responses.GET,
        http_client._base_url + "/balance",
        json={"amount": 50.5, "currency": "usd"},
        status=200
    )

    balance_service = BalanceService(http_client)

    # act
    balance = balance_service.get()

    # assert
    assert type(balance) == Balance
    assert type(balance.amount) == float
    assert type(balance.currency) == str
    assert balance.amount == 50.5
    assert balance.currency == "usd"
