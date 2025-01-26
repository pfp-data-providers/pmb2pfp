start_time=$(date +%s)

python scripts/pmb_orgs.py
python scripts/pmb_places.py
python scripts/pmb_persons.py
python scripts/pmb_person_person_relations.py
python scripts/pmb.py

end_time=$(date +%s)
duration=$((end_time - start_time))
formatted_duration=$(printf '%02dh:%02dm:%02ds\n' $(($duration/3600)) $(($duration%3600/60)) $(($duration%60)))

numberoflines=$(wc -l < datasets/pmb.nt)
formatted_number=$(printf "%'d" $numberoflines)

echo "Created PMB Dataset with ${formatted_number} triples in ${formatted_duration}"
