"""
1. Delete the tax with the given ID
2. If the tax is not in the DB, return 404
3. If the user is not authenticated, return 401
/tax/{tax_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_tax(client, tax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/tax/{tax.id}", headers=headers)

    assert response.status_code == 200


def test_delete_tax_not_existing(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/tax/-1", headers=headers)

    assert response.status_code == 404


def test_delete_tax_not_authorized(client, tax):
    response = client.delete(f"/tax/{tax.id}")

    assert response.status_code == 401
