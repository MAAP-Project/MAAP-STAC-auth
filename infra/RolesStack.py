from aws_cdk import (
    aws_iam as iam,
    CfnOutput,
    Stack,
)
import boto3
from constructs import Construct

DATA_PIPELINE_LAMBDA_EXECUTION_ROLE_PATTERN = "maap-data-pipelines-*-datapipelinelambdarole*"
STAC_INGESTOR_EXECUTION_ROLE_PATTERN = 'stacingestor'

class RolesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.create_data_access_role()

        # export a cloud formation output with the data access role name and arn
        CfnOutput(
            self,
            "data access role arn",
            export_name=f"data-access-role-arn",
            value=self.data_access_role.role_arn
        )
            
    def create_data_access_role(
        self
    ):
        """
        Creates data access role, attaches inline policy to allow access to s3 buckets, and grants assume role to data pipeline and stac ingestor roles
        """
        
        role = iam.Role(
            self,
            "data-access-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
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
                "bucket-access-policy",
                statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=["s3:ListBucket*", "s3:GetObject*"],
                        resources=[f"arn:aws:s3:::{bucket}" for bucket in buckets],
                    )
                ],
            )
        )
        
        account_id = boto3.client("sts").get_caller_identity().get("Account")

        role.assume_role_policy.add_statements(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["sts:AssumeRole"],
                conditions={
                    "StringLike": {
                        "aws:PrincipalArn": [
                            f"arn:aws:iam::{account_id}:role/{DATA_PIPELINE_LAMBDA_EXECUTION_ROLE_PATTERN}",
                            f"arn:aws:iam::{account_id}:role/{STAC_INGESTOR_EXECUTION_ROLE_PATTERN}"
                        ]
                    }
                }
            )
        )
        
        self.data_access_role = role
        