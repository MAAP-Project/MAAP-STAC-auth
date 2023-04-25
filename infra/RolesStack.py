from typing import Optional


from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    CfnOutput,
    Stack,
)
from constructs import Construct

class RolesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, data_pipeline_role_name: str, stac_ingestor_role_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.create_data_access_role(construct_id=construct_id, data_pipeline_role_name=data_pipeline_role_name, stac_ingestor_role_name=stac_ingestor_role_name)

        # export a cloud formation output with the data access role name and arn
        CfnOutput(
            self,
            "data access role name",
            export_name=f"data-access-role-name-{self.stack_name}",
            value=self.data_access_role.role_name
        )
            
    def create_data_access_role(
        self, construct_id: str, data_pipeline_role_name: str, stac_ingestor_role_name: str
    ):
        """
        Creates data access role, attaches inline policy to allow access to s3 buckets, and grants assume role to data pipeline and stac ingestor roles
        """
        
        role_assume = iam.CompositePrincipal(iam.ServicePrincipal("lambda.amazonaws.com"))
        
        role = iam.Role(
            self,
            f"{construct_id}-data-access-role",
            role_name=f"{construct_id}-data-access-role",
            assumed_by=role_assume,
        )
        
        buckets = [
                "nasa-maap-data-store",
                "maap-user-shared-data",
                "maap-ops-workspace",
                "maap-data-store-test",
                "nasa-maap-data-store/*",
                "maap-user-shared-data/*",
                "maap-ops-workspace/*",
                "maap-data-store-test/*"
            ]
        
        role.attach_inline_policy(
            iam.Policy(
                self,
                "Policy",
                statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=["s3:PutObject*", "s3:ListBucket*", "s3:GetObject*"],
                        resources=[f"arn:aws:s3:::{bucket}" for bucket in buckets],
                    )
                ],
            )
        )
        
        data_pipeline_role = iam.Role.from_role_name(self, 'data-pipeline-role', data_pipeline_role_name)
        
        stac_ingestor_role = iam.Role.from_role_name(self, 'stac-ingestor-role', stac_ingestor_role_name)
        
        role.grant_assume_role(data_pipeline_role)
        role.grant_assume_role(stac_ingestor_role)
        
        self.data_access_role = role
        