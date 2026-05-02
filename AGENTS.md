# AGENTS.md

## Project

`hr_interrao_api` is a Flask API for an HR portal. Keep changes small, explicit, and aligned with the existing layered architecture.

## Stack

- Python 3.11+.
- Flask 3.x with the application factory in `app/__init__.py`.
- Flask-SQLAlchemy / SQLAlchemy 2 typed ORM style.
- `uv` is the preferred dependency manager.
- `pytest` is the test runner.
- `ruff` is used for linting and formatting.

## Commands

- Install dependencies with dev tools: `uv sync --dev`.
- Run the app locally: `uv run python main.py`.
- Run tests: `uv run pytest`.
- Run linting: `uv run ruff check .`.
- Format code: `uv run ruff format .`.

## Architecture

Follow the existing module split:

- `api.py`: Flask route handlers, request parsing, response status codes.
- `query.py`: query-string parsing and validation.
- `services.py`: business orchestration and DTO construction.
- `repositories.py`: SQLAlchemy query construction and persistence access.
- `models.py`: SQLAlchemy ORM models.
- `dto.py`: immutable response DTOs and serialization helpers.

Register routes through blueprints under `app/blueprints/`. Keep `main.py` as a thin local entrypoint.

Use existing service builders such as `build_user_service()` and `build_worker_service()` unless introducing a broader dependency-injection pattern is part of the requested task.

## API Rules

- Use `HTTPMethod` and `HTTPStatus` instead of raw method/status strings or integers.
- Return Flask responses as `(jsonify(...), HTTPStatus.X)` tuples, matching existing handlers.
- Keep API routes under `/api/v1/` through the existing `account_bp` and `parus_bp` blueprints.
- Response messages may be Russian; keep wording consistent with nearby endpoints.
- Do not put SQLAlchemy query logic in route handlers.

## Database Rules

- Use `app.settings.database.db`, `BaseModel`, and `get_db_session()`.
- Write SQLAlchemy 2 style models with `Mapped[...]` and `mapped_column(...)`.
- Prefer `select(...)`, `session.scalar(...)`, and `session.scalars(...)` over legacy query APIs.
- Keep current database boundaries:
  - account models use schema `account`;
  - parus/authorization models use `__bind_key__ = "authorization"`.
- Avoid implicit commits in repositories unless the feature is specifically a write operation and tests cover it.

## DTOs And Serialization

- Response DTOs should be `@dataclass(frozen=True, slots=True)` where practical.
- Keep serialization explicit through `to_dict()`.
- Do not return ORM models directly from API handlers.
- Keep UUID values as `UUID` objects internally; convert only at serialization boundaries when needed.

## Python Style

- Use modern type hints: `str | None`, `tuple[...]`, `Sequence[...]`, `Mapping[...]`.
- Prefer imports from `collections.abc` for collection protocols.
- Preserve the existing Russian docstring style for public project functions/classes.
- Keep functions small and names descriptive.
- Add comments only for non-obvious behavior.
- Do not introduce broad abstractions unless they remove real duplication in this codebase.

## Tests

- Put tests under `tests/unit/...` following the package/module being tested.
- Use pytest fixtures from `tests/conftest.py`.
- For API changes, add or update client tests and assert both status code and JSON payload.
- For config changes, pass explicit `env={...}` to `load_config(...)` where possible.
- If behavior changes around query validation, pagination, SQL filters, or DTO mapping, add focused unit tests.

## Configuration And Secrets

- Do not commit real secrets or environment-specific database URLs.
- Keep environment variable names in config classes and resolve them through `load_config(...)`.
- Use `.env` only for local development.

## Change Discipline

- Prefer targeted edits that match nearby code.
- Do not rewrite unrelated modules while implementing a feature.
- Do not revert user changes unless explicitly requested.
- If an existing test appears stale, update it only when the requested change touches that behavior, and keep the update explicit.
