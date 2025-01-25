#!/bin/bash

SHACL=datasets/myshapes.ttl
rm ${SHACL}
curl -o ${SHACL} https://pfp-schema.acdh-ch-dev.oeaw.ac.at/shacl/shacl.ttl
docker run --rm -v ${PWD}/datasets:/data ghcr.io/ashleycaselli/shacl:latest validate -datafile /data/pmb.nt -shapesfile /data/myshapes.ttl > validation_report.txt