#!/bin/bash

echo "Converting pmb.nt to pmb.ttl"
docker run --rm -v ${PWD}/datasets:/rdf stain/jena riot --output=TURTLE pmb.nt > ${PWD}/datasets/pmb.ttl