#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.AuthStack import AuthStack
from infra.RolesStack import RolesStack
from config import Config

config = Config(_env_file=os.environ.get("ENV_FILE", ".env"))

app = cdk.App()
auth_stac = AuthStack(
    app,
    f"MAAP-STAC-auth-{config.stage}",
    ade_iam_role=config.ade_iam_role,
    tags={
        "Project": "MAAP",
        "Owner": config.owner,
        "Client": "NASA",
        "Stack": config.stage,
    },
)


# Generate a resource server (ie something to protect behind auth) with scopes
# (permissions that we can grant to users/services).
stac_registry_scopes = auth_stac.add_resource_server(
    "MAAP-STAC-ingestion-registry",
    supported_scopes={
        "stac:register": "Create STAC ingestions",
        "stac:cancel": "Cancel a STAC ingestion",
        "stac:list": "Cancel a STAC ingestion",
    },
)


# Generate a client for a service, specifying the permissions it will be granted.
# In this case, we want this client to be able to only register new STAC ingestions in
# the STAC ingestion registry service.
auth_stac.add_service_client(
    config.stac_register_service_id,
    scopes=[
        stac_registry_scopes["stac:register"],
    ],
)

# Programmatic Clients
# auth_stac.add_user_client("MAAP-sdk")


# create roles stack
auth_stac = RolesStack(
    app,
    f"MAAP-STAC-roles-{config.stage}",
    tags={
        "Project": "MAAP",
        "Owner": config.owner,
        "Client": "NASA",
        "Stack": config.stage,
    }
)

app.synth()
