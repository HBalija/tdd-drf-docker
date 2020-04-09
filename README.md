## Django DRF Rest API with TDD using Docker and Travis CI

### Quickstart

Get the source from github:

    git clone git@github.com:HBalija/tdd-drf-docker.git

Navigate to project folder:

    cd tdd-drf-docker

Build image from Dockerfile:

    docker build .

Build project with compose:

    make build

Run project (with db migrations):

    make up

Run tests:

    make test
