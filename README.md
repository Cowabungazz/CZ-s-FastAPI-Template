# FastAPI-Template
Tee Chang Zen's FastAPI Template for Local Development

Consistent configs, routing, error handling, and database access. At startup we load configuration from an INI file plus environment variables using pydantic. 

BaseSettings — secrets (e.g., DB passwords, API keys) only come from env and are never checked into git. The app is organized in clean layers. 

Routers live under src/main/routers: I use fastapi-utils class-based views and a central __init__.py that predefines standard response models (HTTP 200 and 500) so every endpoint returns the same envelope: {status_code, version, msg, data}. There’s a /healthy route in monitor.py so k8s can probe liveness. A sample feature router, router1.py, shows the pattern: validate the request with Pydantic base models, call a service layer (service_a) for business logic, use a utils helper where needed, and then persist via a thin data access layer. 

For databases I wrapped an Oracle client in ConnectionInstance and exposed an opinionated DataRetriever with simple methods like insertdb() and finddb*(). Other modules import those via services/oracle/modules.py, which gives us one place to manage connections and retries. 

I also wrote a decorator, @handle_except, that catches any raised exception, captures the file, function, and line number, and returns a uniform InternalServerErrorModel — that ended a lot of ad-hoc error shapes and made on-call debugging faster. The handle_resp() helper standardizes successful responses, and a required_headers dependency enforces per-request metadata (e.g., tenant or correlation id).

# config init
If you plan to expose more sections (e.g., Database, Cache), follow the ApConfig pattern: read defaults from INI, then use validation_alias for env overrides.

Ensure your get_settings() exposes DB fields (dsn/user/password). If you store a DSN URL, parse it once here.

## How to use? 
```
from src.main.config import get_settings
settings = get_settings()
```

# src\requirements.txt
Tip: For reproducible builds, keep this fully pinned and use a periodic job to refresh pins.

# src\main\main.py
Update router imports if your package path is src.main.python.routers. Prefer one canonical path (e.g., src.main.routers) across the codebase.

settings comes from your Pydantic v2 config (get_settings()); make sure it exposes app_version, host, port, workers, log_level, etc.

required_headers enforces headers only in production as an example—tune to your needs.

# cURL
curl -X POST "http://0.0.0.0:8000/router1/posturl" \
  -H "Content-Type: application/json" \
  -H "header_1: value1" \
  -H "header_2: value2" \
  -d @payload.json

# src\main\schemas
Replace Router1BaseModel, Router1ResponseModel, SuccessResponseModel, InternalServerErrorModel with the real Pydantic models.

# src\main\services\oracle\
## DB_Interface.py
Parameter binding: Adjust :1, :2 placeholders to match your driver (e.g., :name binds).
## MakeConnection.py
Replace MakeConnection’s placeholders with a real pool/driver (oracledb, cx_Oracle) and return actual rows.

Errors: Let the DB layer raise specific exceptions; convert them to your API error model in the router decorators.

Testing: For unit tests, monkeypatch db_api or inject a fake MakeConnection into DB_Interface.

# azure-pipelines.yaml
Use a Service Connection named MyContainerRegistryServiceConnection pointing to your Harbor/ACR registry.

The push step runs only on main. Adjust as needed.

# CI/CD
Pin versions in requirements.txt for reproducible builds.

Do not bake real secrets or .env into the release image—inject via CI/CD or orchestration.

Configure an Azure DevOps Service Connection to your container registry (Harbor/ACR) and update imageRepository.

If your app module isn’t src.main.app:app, tweak the CMD in the Dockerfile accordingly.
