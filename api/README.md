## Initial Setup

1. setup a new database with connection_string=postgresql://postgres@localhost/nomorewait
2. Run DB migration: `make migrate`
3. Load initial data: `python3 app/initial_data.py`

## DB Migration

- To autogenerate migration script:  
  `make migration MESSAGE=<description>`

- To migrate:  
  `make migrate`

- To rollback:  
  `make rollback`
