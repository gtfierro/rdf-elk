DOCKER_BUILDKIT=1 docker build --network=host -t rdf-elk:latest .
docker save rdf-elk:latest | gzip > rdf-elk.tar.gz
scp rdf-elk.tar.gz webserver:.
#docker run --rm -p 5000:5000 rdf-elk:latest
