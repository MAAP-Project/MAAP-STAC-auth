#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.stack import AuthStack
from config import Config

config = Config(_env_file=os.environ.get("ENV_FILE", ".env"))

app = cdk.App()
stack = AuthStack(
    app,
    f"{config.stack_base}-{config.stage}",
    tags={
        "Project": "MAAP",
        "Owner": config.owner,
        "Client": "NASA",
        "Stack": config.stage,
    },
)


# Generate a resource server (ie something to protect behind auth) with scopes
# (permissions that we can grant to users/services).
stac_registry_scopes = stack.add_resource_server(
    "MAAP-stac-ingestion-registry",
    supported_scopes={
        "stac:register": "Create STAC ingestions",
        "stac:cancel": "Cancel a STAC ingestion",
        "stac:list": "Cancel a STAC ingestion",
    },
)


# Generate a client for a service, specifying the permissions it will be granted.
# In this case, we want this client to be able to only register new STAC ingestions in
# the STAC ingestion registry service.
stack.add_service_client(
    config.stac_register_service_id,
    scopes=[
        stac_registry_scopes["stac:register"],
    ],
)

# Programmatic Clients
# stack.add_user_client("MAAP-sdk")

app.synth()
