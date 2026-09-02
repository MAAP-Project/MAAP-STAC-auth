# MAAP Auth System

This codebase stores the IaC for authentication and common IAM roles used for the MAAP STAC infrastructure.

Note : Managing individual cognito users should be done via the console.

## Contributing

### 1. Prerequisites

First, ensure you have [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) installed. You can install it using one of the official commands:

* **pip:** Suggested: `pipx install uv` or `pip install uv`
* **Homebrew:** `brew install uv`
* **macOS/Linux:** `curl -LsSf https://astral.sh | sh`
* **Windows:** `powershell -c "irm https://astral.sh | iex"`

### 2. Development Setup

1. **Fork and clone** the repository.
2. **Install project dependencies** (this automatically sets up a virtual environment):

   ```bash
   uv sync
   ```

3. **Install the pre-commit hooks** so your code is automatically linted before every commit:

   ```bash
   uv run pre-commit install
   ```

### 3. Verification Commands

* **Manually run lints across all files:**

  ```bash
  uv run pre-commit run --all-files
  ```

## Cognito resources

### Running the example service client

This example script provides you with credentials based on service authentication.

```bash
uv run scripts/service-auth-example.py
```

### Expanding

The codebase intends to be expandable to meet MAAP's needs as the project grows. Currently, the stack exposes two methods to facilitate customization.

#### Adding a Resource Server

A resource server is a service that is to be protected by auth.

#### `stack.add_programmatic_client(client_identifier)`

The intention of this endpoint is to create a client for a user to make use of when authenticating in a programmatic environment (e.g. script, notebook).

#### `stack.add_service_client(client_identifier)`

Add a service that will be authenticating with the MAAP system. This utilizes the [`client_credentials` flow](https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/), meaning that the credentials represent a _service_ rather than any particular _user_.
