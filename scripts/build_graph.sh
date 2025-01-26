python scripts/pmb_orgs.py
python scripts/pmb_places.py
python scripts/pmb_persons.py
python scripts/pmb_person_person_relations.py
python scripts/pmb.py

numberoflines=$(wc -l < datasets/pmb.nt)
formatted_number=$(printf "%'d" $numberoflines)
echo "PMB Dataset with ${formatted_number} triples"