import time

import requests

from tests.integration_tests.helpers import API_URL


def test_create_user_group(products):
    group_name = "Group One"

    user_group_id = products["UserGroup"]

    create_response = requests.post(
        f"{API_URL}/processes/create_user_group",
        json=[{"product": user_group_id}, {"group_name": group_name}],
    )

    assert create_response.ok

    process_id = create_response.json()["id"]

    create_wf = None

    for _ in range(3):
        status_response = requests.get(f"{API_URL}/processes/{process_id}")
        assert status_response.ok
        create_wf = status_response.json()
        if create_wf["status"] == "completed":
            break
        time.sleep(1)

    assert create_wf["status"] == "completed"

    subscription_id = create_wf["subscriptions"][0]["subscription_id"]

    domain_model_response = requests.get(
        f"{API_URL}/subscriptions/domain-model/{subscription_id}"
    )
    assert domain_model_response.ok
    domain_model = domain_model_response.json()

    assert domain_model["description"] == f"User Group {group_name}"
    assert domain_model["product"]["name"] == "User Group"
    assert domain_model["user_group"]["group_name"] == group_name
