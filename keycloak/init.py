import ast
from os import environ

# from keycloak import KeycloakAdmin
# from keycloak import KeycloakOpenIDConnection
from urllib.parse import urljoin

import requests
import time

BASE_URL = "http://keycloak:8080/"


def print_response(response):
    for key, val in vars(response).items():
        print(f"{key}: {val}")

def check_health():
    path = "health"
    url = urljoin(BASE_URL, path)

    try:
        x = requests.get(url)
        return True
    except requests.exceptions.ConnectionError:
        return False


def get_token():
    path = "realms/master/protocol/openid-connect/token"
    url = urljoin(BASE_URL, path)

    params = {
        "client_id": "admin-cli",
        "grant_type": "password",
        "username": "admin",
        "password": "admin",
    }
    x = requests.post(url, params, verify=False).content.decode("utf-8")
    return ast.literal_eval(x)["access_token"]


def create_realm(name, token=None):
    print("CREATING REALM:")
    path = "admin/realms"
    url = urljoin(BASE_URL, path)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "id": name,
        "realm": name,
        "displayName": name,
        "enabled": True,
        "sslRequired": "external",
        "registrationAllowed": False,
        "loginWithEmailAllowed": True,
        "duplicateEmailsAllowed": False,
        "resetPasswordAllowed": False,
        "editUsernameAllowed": False,
        "bruteForceProtected": True,
    }
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        if response.status_code == 409:
            if response.text == '{"errorMessage":"Conflict detected. See logs for details"}':
                print(f"Realm '{name}' already exists")
        else:
            print(f"Could not create realm {name}")
            print_response(response)
    else:
        print(f"Realm '{name}' created")


def create_user(realm, username, email="", first_name="", last_name="", token=None):
    print("CREATING USER:")

    path = f"admin/realms/{realm}/users"
    url = urljoin(BASE_URL, path)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "username": f"{username}",
        "email": f"{email}",
        "firstName": f"{first_name}",
        "lastName": f"{last_name}",
        "requiredActions": [],
        "emailVerified": False,
        "groups": [],
        "enabled": True,
        "attributes": {"hoi": ["hoi"]},
    }
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        if response.status_code == 409:
            print(f"User '{username}' already exists in realm {realm}")
        else:
            print_response(response)
    else:
        print(f"User '{username}' created in realm {realm}")


def get_user(realm, username, token=None):
    print(f"GETTING USER: {username}")
    path = f"admin/realms/{realm}/ui-ext/brute-force-user"
    url = urljoin(BASE_URL, path)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    result = None
    if not response.ok:
        print(f"Get user {username} failed")
        print_response(response)
    else:
        user_dict = response.json()
        result = next(user for user in user_dict if user["username"] == username)
    # import pprint; pprint.pprint(client_scope_dict)
    return result


def get_user_credentials(realm, user_id, token=None):
    print("GETTING USER CREDENTIALS:")

    type(f"user: {user_id}")
    path = f"admin/realms/{realm}/users/{user_id}/credentials"
    url = urljoin(BASE_URL, path)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    result = None
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(f"Get user credentials for user_id {user_id} failed.")
        print_response(response)
    else:
        print(f"Succesfully got user credentials for user_id {user_id}.")
        result = response.json()[0]
    return result


def add_user_label(realm, user_id, label="My password", token=None):
    print("ADD USER LABEL:")
    credentials_id = get_user_credentials(realm, user_id, token=token)["id"]
    path = f"admin/realms/development/users/{user_id}/credentials/{credentials_id}/userLabel"
    url = urljoin(BASE_URL, path)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "plain/text",
    }

    response = requests.put(url, headers=headers, data=label)
    if not response.ok:
        print(f"Adding label to credentials {credentials_id} failed.")
        print_response(response)
    else:
        print(f"Succesfully added label to credentials {credentials_id}.")


def set_user_password(realm, username, password, token=None):
    print("SET USER PASSWORD:")

    user_id = get_user(realm, username, token=token)["id"]
    path = f"admin/realms/development/users/{user_id}/reset-password"
    url = urljoin(BASE_URL, path)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {"temporary": False, "type": "password", "value": password}

    response = requests.put(url, headers=headers, json=data)
    add_user_label(realm, user_id, token=token)
    if not response.ok:
        print_response(response)
        # if response.status_code == 500:
        #     if "unknown_error" in response.text:
        #         print(f"Looks like mapper '{mapper_name}' already exists in scope {scope_name}")
        # else:
        #     print(f"Could not add mapper {mapper_name}")
        #     print_response(response)
    else:
        print(f"Password set for user '{username}' in realm {realm}")


def create_client_orchestrator(realm, client_id, name, token=None):
    print("CREATING CLIENT OIDC-PROXY:")
    path = f"admin/realms/{realm}/clients"
    url = urljoin(BASE_URL, path)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "protocol": "openid-connect",
        "clientId": f"{client_id}",
        "name": f"{name}",
        "description": "",
        "publicClient": True,
        "authorizationServicesEnabled": False,
        "serviceAccountsEnabled": False,
        "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": False,
        "standardFlowEnabled": True,
        "frontchannelLogout": True,
        "attributes": {
            "saml_idp_initiated_sso_url_name": "",
            "oauth2.device.authorization.grant.enabled": False,
            "oidc.ciba.grant.enabled": False,
        },
        "alwaysDisplayInConsole": True,
        "rootUrl": "",
        "baseUrl": "",
        "redirectUris": ["*"],
        "webOrigins": ["*"],
    }

    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        if response.status_code == 409:
            if "already exists" in response.text:
                print(f"Client '{client_id}' already exists in realm {realm}")
        else:
            print(f"Could not create client {client_id}")
            print_response(response)
    else:
        print(f"Client '{name}' created")


if __name__ == "__main__":
    realm = "development"
    scope = "SURF"

    while not check_health():
        print("Waiting for keycloak health ok")
        time.sleep(2)
    print("Get token for keycloak api")
    token = get_token()
    print("Add realm development")
    create_realm(realm, token=token)
    print("Creating user test-user")
    create_user(realm, "test-user", "test-user@orchestrator-gui.com", "test", "user", token=token)
    print("Set password for user test-user")
    set_user_password(realm, "test-user", "xxx", token=token)
    print("Creating client orchestrator")
    create_client_orchestrator(
        realm,
        "orchestrator-gui.localhost",
        "Orchestrator",
        token=token,
    )
