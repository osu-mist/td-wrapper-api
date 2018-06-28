# Long Description

This script is used return all services, but include their long descriptions (with HTML tags and such).

## Instructions

Copy [configuration-example.py](configuration-example.py) to configuration.py and modify as needed.

### Run with Docker
```
docker build -t long_description .
docker run --rm -it -v "$PWD"/configuration.py:/usr/src/long-description/configuration.py:ro --name='long_description' long_description
docker cp long_description:/usr/src/long-description/services.json .
docker rm long_description
```
