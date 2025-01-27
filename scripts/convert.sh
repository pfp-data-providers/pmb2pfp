#!/bin/bash
start_time=$(date +%s)

DATA_DIR=datasets
NT=pmb.nt
TTL=pmb.ttl

echo "Converting pmb.nt to pmb.ttl"

NT_SIZE=$(du -h ${DATA_DIR}/${NT})
docker run --rm -v ${PWD}/datasets:/rdf stain/jena riot --output=TURTLE ${NT} > ${PWD}/${DATA_DIR}/${TTL}
TTL_SIZE=$(du -h ${DATA_DIR}/${TTL})

end_time=$(date +%s)
duration=$((end_time - start_time))
formatted_duration=$(printf '%02dh:%02dm:%02ds\n' $(($duration/3600)) $(($duration%3600/60)) $(($duration%60)))

echo "Converted ${NT} (${NT_SIZE}) to ${TTL} (${TTL_SIZE}) in ${formatted_duration}"