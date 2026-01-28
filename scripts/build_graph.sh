start_time=$(date +%s)

DATA_FOLDER=datasets
PERSON_PERSON="pmb-person-person.xml"

rm -rf ${DATA_FOLDER}
mkdir ${DATA_FOLDER}
echo "saving https://pmb.acdh.oeaw.ac.at/network/tei/?edge_kind=personperson as ${PERSON_PERSON}"

wget -O ${PERSON_PERSON} https://pmb.acdh.oeaw.ac.at/network/tei/?edge_kind=personperson

uv run scripts/person_org_relations.py
uv run scripts/bibls.py
uv run scripts/orgs.py
uv run scripts/bibls.py
uv run scripts/places.py
uv run scripts/persons.py
uv run scripts/person_person_relations.py
uv run scripts/finalize.py

end_time=$(date +%s)
duration=$((end_time - start_time))
formatted_duration=$(printf '%02dh:%02dm:%02ds\n' $(($duration/3600)) $(($duration%3600/60)) $(($duration%60)))

numberoflines=$(wc -l < datasets/pmb.nt)
formatted_number=$(printf "%'d" $numberoflines)

echo "Created PMB Dataset with ${formatted_number} triples in ${formatted_duration}"
