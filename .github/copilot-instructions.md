# AI Agent Instructions for user_management

## Project Overview
A Python backend user management system for authentication, session handling, and user administration. This is a learning/practice project using SQLAlchemy ORM with PostgreSQL.

## Architecture

### Layered Structure
```
user_manager/
├── main.py (entry point)
├── app/
│   ├── models.py (SQLAlchemy ORM models)
│   ├── database.py (DB connection & session factory)
│   ├── config.py (configuration - currently empty)
│   └── user_manager.py (business logic - currently empty)
└── tests/ (pytest test suite)
```

### Data Models (app/models.py)
Four core entities with foreign key relationships:
- **User**: username (PK), email (unique), password_hash, role
- **Session**: token (PK), username (FK), expires_at
- **PasswordResetToken**: token (PK), username (FK), expires_at
- **LoginHistory**: id (PK), username (FK), timestamp

All models inherit from `Base` (declarative base) and use SQLAlchemy Column types.

### Database Layer (app/database.py)
- Engine created from `DATABASE_URL` env var (PostgreSQL connection string)
- `SessionLocal = sessionmaker(bind=engine)` for DB operations
- `Base = declarative_base()` for model inheritance
- Always use `.env` for `DATABASE_URL` - currently: `postgresql://postgres:...@localhost:5432/user_manager_db`

## Development Patterns

### Model & ORM Usage
- All models defined in `app/models.py` inherit from `Base`
- Use `Column()` with SQLAlchemy types (String, DateTime, ForeignKey)
- Primary keys: username (User), token (Session/PasswordResetToken), id (LoginHistory)
- Foreign keys enforce referential integrity to User.username
- Import: `from sqlalchemy import ...` and `from app.database import Base`

### Business Logic Placement
- `app/user_manager.py` (currently empty) should contain authentication & user operations
- Separate concerns: models (schema) vs user_manager (behavior)
- Use `SessionLocal()` for database transactions

### Testing
- Tests in `tests/test_user_manager.py` (currently empty)
- Pytest fixtures in `tests/conftest.py` (currently empty)
- Expected test coverage: authentication, session management, password reset flows

## Critical Developer Workflows

### Running the Project
```bash
# Install dependencies (requirements.py empty - add pip freeze output)
pip install sqlalchemy psycopg2-binary python-dotenv pytest

# Set PostgreSQL connection in .env (already configured)
# Database must be running on localhost:5432

# Run main application (main.py entry point - not yet implemented)
python user_manager/main.py

# Run tests
pytest tests/
```

### Database Setup
- PostgreSQL must be accessible at localhost:5432
- Database name: `user_manager_db`
- Credentials in `.env` (avoid committing credentials)
- Schema auto-created from models via SQLAlchemy (implement in main.py: `Base.metadata.create_all(engine)`)

## Integration Points & Dependencies

### External Dependencies (should add to requirements.txt)
- **sqlalchemy**: ORM for model definition and queries
- **psycopg2-binary**: PostgreSQL adapter for SQLAlchemy
- **python-dotenv**: Load DATABASE_URL from .env
- **pytest**: Test framework (for tests/)

### Environment Configuration
- `.env` file: Must contain `DATABASE_URL` for database connection
- Connection format: `postgresql://user:password@host:port/database`
- Loaded via: `from dotenv import load_dotenv` in database.py

## Key Conventions & Gotchas

1. **No Timestamps in User Model**: Add `created_at`, `updated_at` if audit trail needed
2. **Password Hashing**: Implement in user_manager.py (use bcrypt/argon2, never store plaintext)
3. **Token Expiry**: LoginHistory has `timestamp` but Session/PasswordResetToken have `expires_at` - check expiry before operations
4. **Foreign Key Cascade**: Consider deletion policies (cascade vs restrict) when defining ForeignKey(...)
5. **Database Connection**: Always use `SessionLocal()` context manager to avoid connection leaks
6. **Role-Based Access**: User.role field exists (default="user") - implement RBAC in user_manager.py

## Common Tasks

### Adding a New Model
1. Define in `app/models.py` inheriting from `Base`
2. Use `Column()` for fields, `ForeignKey()` for relationships
3. Re-run `Base.metadata.create_all(engine)` to migrate

### Creating User Operations
1. Implement in `app/user_manager.py` using `SessionLocal()`
2. Handle password hashing, token generation
3. Add corresponding tests in `tests/test_user_manager.py`

### Debugging Database Issues
- Verify `.env` DATABASE_URL is correct
- Ensure PostgreSQL service is running
- Check model FK constraints match target tables
- Use SQLAlchemy logging: `echo=True` in create_engine()
