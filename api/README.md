## Initial Setup

1. setup a new database with connection_string=postgresql://postgres@localhost/nomorewait
2. Run DB migration: `make migrate`
3. Load initial data: `make initdata`

## Data Management

- Load initial data: `make initdata`
- Clear all data: `make cleardata`

## DB Migration Management

- To autogenerate migration script: `make migration MESSAGE=<description>`
- To migrate: `make migrate`
- To rollback: `make rollback`
