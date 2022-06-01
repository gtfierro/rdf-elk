DOCKER_BUILDKIT=1 docker build --network=host -t rdf-elk:latest .
docker run --rm -p 5000:5000 rdf-elk:latest
