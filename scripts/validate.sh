#!/bin/bash

DATA_DIR=datasets
REPORT=${DATA_DIR}/validation_report.txt

SHACL=${DATA_DIR}/myshapes.ttl
rm ${SHACL}
echo "downloading latest SHACL shapes"
curl -o ${SHACL} https://pfp-schema.acdh-ch-dev.oeaw.ac.at/shacl/shacl.ttl

echo "Validating pmb.nt against SHACL shapes"
docker run --rm -v ${PWD}/${DATA_DIR}:/data ghcr.io/ashleycaselli/shacl:latest validate -datafile /data/pmb.nt -shapesfile /data/myshapes.ttl > ${REPORT}

echo "Validation report written to ${REPORT}"
VIOLATIONS=$(grep -o "sh:Violation" ${REPORT} | wc -l)
echo "Upsi dupsi, there are ${VIOLATIONS} violations. hush hush, go and fix them!"