# 🎯 API Builder Agent Standards & Requirements

## 📋 Universal Standards (ALL AGENTS MUST FOLLOW)

### 🔐 Version Control & Git Discipline

#### Initial Setup
- **FIRST ACTION**: Ask user if we should create a new GitHub repository
  - Get repository name preference
  - Initialize with proper .gitignore
  - Set up branch protection rules

#### Commit Standards
- **Frequency**: Every 30 minutes minimum
- **Format**: Conventional commits
  ```
  feat(api): Add user authentication endpoints
  fix(db): Resolve connection pool timeout
  docs(api): Update endpoint documentation
  test(auth): Add JWT validation tests
  chore(deps): Update FastAPI to 0.104.1
  ```
- **Push Protocol**: Push to GitHub after every 2-3 commits
- **Branch Strategy**: 
  - `main` - Production ready code
  - `develop` - Integration branch
  - `feature/*` - Feature development
  - `fix/*` - Bug fixes

### 📚 Documentation Requirements

#### Mandatory Files (MAINTAIN CONTINUOUSLY)
```
workspace/
├── implementation_plan.md    # Detailed roadmap with TODO tracking
├── architecture.md          # System design, component relationships
├── api.md                   # Complete API documentation
├── quickstart.md            # Setup and run instructions
├── README.md                # Overview with make commands
├── CHANGELOG.md             # Version history
└── docs/
    ├── deployment.md        # Deployment instructions
    ├── testing.md          # Testing strategy
    ├── monitoring.md       # Observability setup
    └── troubleshooting.md  # Common issues and solutions
```

#### Documentation Standards
- **Real-time Updates**: Update docs with every feature/change
- **No Placeholders**: Never use "TBD" - use specific TODOs with tracking
- **Code Examples**: Include working examples for all features
- **Diagrams**: Use mermaid for architecture diagrams

### 🔧 Configuration Management

#### Environment Variables (MANDATORY)
```bash
# .env.example (commit this)
# .env (never commit - in .gitignore)

# === APPLICATION ===
APP_NAME=api-builder
APP_VERSION=1.0.0
ENVIRONMENT=development  # development|staging|production
DEBUG=true
LOG_LEVEL=INFO

# === API CONFIGURATION ===
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]

# === DATABASE ===
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# === REDIS ===
REDIS_URL=redis://localhost:6379
REDIS_PREFIX=api_builder:

# === AUTHENTICATION ===
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# === MONITORING ===
PROMETHEUS_URL=http://localhost:9090
GRAFANA_URL=http://localhost:3000
LOKI_URL=http://localhost:3100
TEMPO_URL=http://localhost:3200

# === SHARED INFRASTRUCTURE ===
USE_SHARED_STAGING=true
STAGING_PATH=/Users/petermager/Downloads/code/create_staging
```

#### Configuration Rules
- **No Hardcoded Values**: Everything must use environment variables
- **Validation**: Validate all config on startup
- **Defaults**: Provide sensible defaults for development
- **Type Safety**: Use pydantic Settings for config management

### 🐍 Python Standards (CRITICAL)

#### Version Requirements
```bash
# MANDATORY: Python 3.12
export UV_PYTHON=/opt/homebrew/bin/python3.12

# FORBIDDEN: Python 3.13 (pydantic-core compilation issues)
```

#### Package Management
```bash
# requirements.txt - Production dependencies only
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2  # NOT 3.0 - compatibility issues
redis==5.0.1

# requirements-dev.txt - Development dependencies
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
black==23.12.0
ruff==0.1.8
mypy==1.7.1
```

#### Virtual Environment
```bash
# Always use .venv (not venv)
uv venv --python /opt/homebrew/bin/python3.12
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

### 🏗️ Makefile Standards

#### Structure
```makefile
# === Variables ===
UV_PYTHON := /opt/homebrew/bin/python3.12
export UV_PYTHON
UV := uv
PYTHON := $(UV) run python
PROJECT := api-builder

# === Help ===
.PHONY: help
help: ## Show this help message
	@echo "$(PROJECT) - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# === Setup ===
.PHONY: setup
setup: ## Complete project setup
	@echo "Setting up $(PROJECT)..."
	$(MAKE) check-python
	$(MAKE) install
	$(MAKE) setup-db
	$(MAKE) setup-git-hooks

# === Development ===
.PHONY: run
run: ## Run the application
	$(PYTHON) -m app.main

.PHONY: dev
dev: ## Run in development mode with auto-reload
	$(UV) run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# === Testing ===
.PHONY: test
test: ## Run all tests
	$(PYTHON) -m pytest tests/ -v

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	$(PYTHON) -m pytest tests/ --cov=app --cov-report=html --cov-report=term

# === Quality ===
.PHONY: lint
lint: ## Run linting
	$(UV) run ruff check .
	$(UV) run mypy app/

.PHONY: format
format: ## Format code
	$(UV) run black .
	$(UV) run ruff check --fix .

# === Docker ===
.PHONY: docker-build
docker-build: ## Build Docker image
	docker build -t $(PROJECT):latest .

.PHONY: docker-run
docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env $(PROJECT):latest

# === Deployment ===
.PHONY: deploy
deploy: ## Deploy to Kubernetes
	kubectl apply -f k8s/

# === Utilities ===
.PHONY: clean
clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/
```

### 🧪 Testing Requirements

#### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
├── fixtures/      # Test fixtures
├── conftest.py    # Pytest configuration
└── test_config.py # Test configuration
```

#### Testing Standards
- **Coverage Target**: Minimum 80% (configurable)
- **Test Types**: Unit, Integration, E2E
- **Naming**: `test_<functionality>_<scenario>.py`
- **Fixtures**: Use pytest fixtures for reusable test data
- **Mocking**: Mock external services appropriately
- **CI/CD**: All tests must pass before merge

### 🔍 Monitoring & Observability

#### Logging Standards
```python
# Dual logging configuration
import logging
import json
from pythonjsonlogger import jsonlogger

# Console logger (human-readable)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

# Prometheus/Loki logger (JSON)
json_handler = logging.StreamHandler()
json_handler.setFormatter(jsonlogger.JsonFormatter())

# Frontend logs passed to backend
@app.post("/api/logs")
async def frontend_log(log_data: dict):
    logger.info("Frontend log", extra={"frontend": log_data})
```

#### Metrics & Dashboards
- **Prometheus Metrics**: Export application metrics
- **Grafana Dashboards**: Create detailed visualizations
- **Alerts**: Configure proactive alerting
- **Tracing**: Implement distributed tracing with Tempo

### 🏭 Shared Infrastructure Usage

#### Available Services
```yaml
# Connection strings for local development
services:
  redis: redis://localhost:6379
  postgres: postgresql://staging_user:staging_password_change_me@localhost:5432/staging_db
  grafana: http://localhost:3000  # admin/admin
  prometheus: http://localhost:9090
  loki: http://localhost:3100
  tempo: http://localhost:3200

# Docker network names
networks:
  - staging_network
```

#### Usage Pattern
```bash
# Start shared infrastructure
cd /Users/petermager/Downloads/code/create_staging
make up

# Use in docker-compose.yml
networks:
  staging_network:
    external: true
```

### 🚫 Anti-Patterns (NEVER DO THESE)

1. **NO Mock Functions**: Use TODO markers and track in implementation_plan.md
2. **NO Hardcoded Values**: Everything must be configurable
3. **NO Uncommitted Code**: Commit every 30 minutes
4. **NO Untested Code**: Write tests for every feature
5. **NO Manual Operations**: Everything through Makefile
6. **NO Python 3.13**: Use Python 3.12 exclusively
7. **NO Missing Documentation**: Update docs in real-time
8. **NO Direct Database Access**: Always use ORM/repository pattern

### ✅ Quality Gates

Before marking ANY task complete:
1. ✅ Tests written and passing (coverage met)
2. ✅ Documentation updated (all relevant files)
3. ✅ Code reviewed (self-review minimum)
4. ✅ Makefile targets created/updated
5. ✅ Environment variables used
6. ✅ Error handling comprehensive
7. ✅ Logging implemented (dual format)
8. ✅ Git committed with meaningful message
9. ✅ No TODO items without tracking
10. ✅ Performance acceptable (<2s response time)

### 📊 MCP Server Specific Requirements

#### Testing Protocol
```bash
# Required tests before deployment
make mcp-test-comprehensive  # 23 automated tests
make mcp-test-interactive    # Manual testing
make mcp-test-concurrent     # Stress testing
make mcp-test-report         # Generate report

# Performance requirements
- Response time < 2 seconds
- Concurrent requests ≥ 10
- Memory usage stable
- No memory leaks
```

#### Claude Desktop Integration
```json
{
  "mcpServers": {
    "api-builder": {
      "command": "python",
      "args": ["-m", "app.mcp_server"],
      "env": {
        "LOG_FILE": "",
        "PYTHONPATH": "."
      }
    }
  }
}
```

### 🎯 API Development Standards

#### FastAPI Structure
```python
# Clean microservice-like API design
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI(
    title="API Builder",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Request/Response models
class UserRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

# Dependency injection
async def get_db():
    # Database session management
    pass

# Clean endpoint design
@app.post("/api/v1/users", response_model=UserResponse)
async def create_user(
    user: UserRequest,
    db: AsyncSession = Depends(get_db)
):
    # Implementation
    pass
```

#### Error Handling
```python
from fastapi import HTTPException

class APIError(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str):
        super().__init__(
            status_code=status_code,
            detail={"message": detail, "error_code": error_code}
        )

# Usage
raise APIError(400, "Invalid input", "VALIDATION_ERROR")
```

### 🎨 Frontend Standards (If React Required)

#### Technology Stack
- **Language**: TypeScript (mandatory)
- **Real-time**: WebSockets for live updates
- **Tables**: ag-Grid for data tables
- **Charts**: Plotly for visualizations
- **HTTPS**: Default configuration

#### Component Design
```typescript
// Simple, testable components
interface Props {
  data: UserData[];
  onUpdate: (id: string) => void;
}

export const UserList: React.FC<Props> = ({ data, onUpdate }) => {
  // Component logic
};

// Comprehensive testing
describe('UserList', () => {
  it('should render user data', () => {
    // Test implementation
  });
});
```

### 🚀 CI/CD Requirements

#### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Run tests
        run: make test
      - name: Check coverage
        run: make test-coverage
```

#### Deployment Scripts
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-builder
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-builder
  template:
    metadata:
      labels:
        app: api-builder
    spec:
      containers:
      - name: api
        image: api-builder:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: production
```

## 📝 Agent-Specific Focus Areas

### Lead Developer
- Repository setup and management
- Architecture decisions
- Team coordination
- Documentation oversight
- Quality enforcement

### FastAPI Developer
- RESTful API design
- Database models (SQLAlchemy)
- Authentication/Authorization
- Request validation
- Error handling

### MCP Server Developer
- Claude Desktop integration
- Tool implementation
- Protocol compliance
- Python 3.12 compatibility
- Testing with mcp-use

### Make Command Builder
- Comprehensive Makefile
- Script organization
- Cross-platform compatibility
- CI/CD integration
- Deployment automation

### Documentation Developer
- API documentation
- User guides
- Architecture diagrams
- Changelog maintenance
- Example code

### E2E Tester
- Test coverage (80%+)
- Pytest implementation
- Fixture creation
- Integration testing
- Performance testing

### Jupyter Developer
- Interactive notebooks
- API testing examples
- Data visualization
- Tutorial creation
- Documentation notebooks

## 🎉 Success Criteria

The project is successful when:
1. ✅ All tests passing with >80% coverage
2. ✅ Complete API documentation at /api/docs
3. ✅ All operations available via Makefile
4. ✅ Docker image builds and runs
5. ✅ K8s deployment scripts working
6. ✅ MCP server passes all tests
7. ✅ Monitoring dashboards configured
8. ✅ Documentation complete and current
9. ✅ GitHub repository with CI/CD
10. ✅ No hardcoded values or mock functions