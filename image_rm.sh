#!/bin/bash

images=(
    "nofacexquestions-discord_bot:latest"
    "nofacexquestions-flask_frontend:latest"
    "nofacexquestions-flask_backend:latest"
)

for image in "${images[@]}"; do
    docker image rm $image
done
