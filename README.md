# MAAP Auth System

This codebase stores the IaC for authentication and common IAM roles used for the MAAP STAC infrastructure.

Note : Managing cognito users should be done via the console.

## Deploying

### Requirements

- `docker` is running
- the AWS CDK CLI is installed
- verify the configuration in `.env`. 

Run : 
- `cdk synth --all`
- `cdk deploy --all`

## Cognito resources

### Running the example service client

This example script provides you with credentials based on service authentication.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/service-auth-example.py
```

### Expanding

The codebase intends to be expandable to meet MAAP's needs as the project grows. Currently, the stack exposes two methods to facilitate customization.

#### Adding a Resource Server

A resource server is a service that is to be protected by auth.

#### `stack.add_programmatic_client(client_identifier)`

The intention of this endpoint is to create a client for a user to make use of when authenticating in a programmatic environment (e.g. script, notebook).

#### `stack.add_service_client(client_identifier)`

Add a service that will be authenticating with the MAAP system. This utilizes the [`client_credentials` flow](https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/), meaning that the credentials represent a _service_ rather than any particular _user_.
