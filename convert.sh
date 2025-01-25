#!/bin/bash

docker run --rm -v -v ${PWD}/datasets:/data apache-jena \
    riot --formatted=TURTLE /data/pmb.nt > /data/pmb.ttl
