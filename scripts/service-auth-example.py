#!/usr/bin/env python3
import json

import boto3
import pydantic
import requests


def get_token(config: "CognitoClientDetails") -> "Creds":
    response = requests.post(
        f"{config.cognito_domain}/oauth2/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        auth=(config.client_id, config.client_secret),
        data={
            "grant_type": "client_credentials",
            # A space-separated list of scopes to request for the generated access token
            "scope": config.scope,
        },
    )
    try:
        response.raise_for_status()
    except Exception:
        print(response.text)
        raise
    return Creds(**response.json())


class CognitoClientDetails(pydantic.BaseModel):
    cognito_domain: str
    client_id: str
    client_secret: str = pydantic.Field(repr=False)
    scope: str


class Creds(pydantic.BaseModel):
    access_token: str
    expires_in: int
    token_type: str


class Settings(pydantic.BaseSettings):
    stage: str
    stac_register_service_id: str

    @property
    def stack_name(self) -> str:
        return f"MAAP-STAC-auth-{self.stage}"

    def get_cognito_service_details(self) -> "CognitoClientDetails":
        client = boto3.client("secretsmanager")
        secret_id = f"{self.stack_name}/{self.stac_register_service_id}"
        try:
            response = client.get_secret_value(SecretId=secret_id)
        except client.exceptions.ResourceNotFoundException:
            raise Exception(
                f"Unable to find a secret for '{secret_id}'. "
                "\n\nHint: Check your stage and service id. Also, verify that the "
                "correct AWS_PROFILE is set on your environment."
            )
        return CognitoClientDetails.parse_obj(json.loads(response["SecretString"]))


if __name__ == "__main__":
    import os

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    os.chdir("../")
    client_details = Settings(
        _env_file=os.environ.get("ENV_FILE", ".env")
    ).get_cognito_service_details()
    credentials = get_token(client_details)
    print(credentials.json())
