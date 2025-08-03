# FastAPI-Template
Tee Chang Zen's FastAPI Template for Local Development

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