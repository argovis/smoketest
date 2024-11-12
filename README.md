This repo contains some very simple scripts to smoke test API changes for consistency and speed.

## Usage

 - in `smoketest.py`, set the URL roots for the current API (`API`) and experimental API (`APIX`)
 - build the image described in `Dockerfile`: `docker image build -t argovis/smoketest:dev .`
 - run from the root dir of this repo, and provide your API key: `docker container run -v $(pwd):/app --env TOKEN=<api key> argovis/smoketest:dev`