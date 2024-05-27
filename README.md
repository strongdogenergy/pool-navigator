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