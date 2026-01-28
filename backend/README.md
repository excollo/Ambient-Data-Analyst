# Ambient Data Analyst Backend

## Running with Docker + Poetry

Build and start the stack (API + Postgres + Redis) from the repo root:

```bash
docker compose up --build
```

Once the containers are up, verify the health endpoints:

```bash
curl http://localhost:8000/internal/healthz
curl http://localhost:8000/v1/health
```

Expected output for both:

```json
{"status":"ok"}
```
