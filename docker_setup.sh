docker run \
  --rm   \
  --name postgres-fastapi \
  -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=collection \
  -d postgres:14.5
sleep 5
docker exec -it postgres-fastapi psql -U postgres