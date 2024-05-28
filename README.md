# pool-navigator
- Startup with `docker compose up` or `docker compose up --build`

## Frontend web - Hugo platform 
- Path `web`
- https://dev.to/robinvanderknaap/setup-hugo-using-docker-43pm or https://gohugo.io/getting-started/quick-start/
- Install hugo and verify `hugo version`
- Create site `hugo new site web`
- Add index.html to layouts folder
- Configure docker compose
```yaml
web:
    image: klakegg/hugo:0.107.0-ext-alpine
    command: server -D --poll 700ms
    volumes:
    - "./web:/src"
    ports:
    - "8001:1313"
```

## Backend API - Python flask app
- Path `api`
- Python source, requirements.txt and Dockerfile
- Configure docker compose
```yaml
api:
    build: ./api
    ports:
        - "8000:5000"
redis:
    image: "redis:alpine"
```

## Google Login
- Following flask tutorial here https://realpython.com/flask-google-login/
```json
{
    "web": {
        "client_id": "195469411341-jg75kao7n2rkuc2i5h1p7j9qut2q3ocb.apps.googleusercontent.com",
        "project_id": "pool-navigator",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "http://localhost:8001/login/callback"
        ],
        "javascript_origins": [
            "http://localhost:8000",
            "http://localhost:8001",
            "http://localhost:5000"
        ]
    }
}
```
- Secrets in .env file
```bash
GOOGLE_CLIENT_ID=195469411341-jg75kao7n2rkuc2i5h1p7j9qut2q3ocb.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
```