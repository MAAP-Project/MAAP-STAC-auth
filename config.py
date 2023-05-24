from getpass import getuser

import pydantic


class Config(pydantic.BaseSettings):
    stage: str = pydantic.Field(
        description=" ".join(
            [
                "Stage of deployment (e.g. 'dev', 'prod').",
                "Used as suffix for stack name.",
                "Defaults to current username.",
            ]
        ),
        default_factory=getuser,
    )
    stac_register_service_id: str = pydantic.Field(
        description=" ".join(
            [
                "name of the service id with the stack:register scope.",
            ]
        ),
        default_factory=getuser,
    )
    owner: str = pydantic.Field(
        description=" ".join(
            [
                "Name of primary contact for Cloudformation Stack.",
                "Used to tag generated resources",
                "Defaults to current username.",
            ]
        ),
        default_factory=getuser,
    )
