# pmb2pfp
repo to serialize pmb-entity-data into pfp-cidoc rdf

This repo fetches data from [PMB](https://pmb.acdh.oeaw.ac.at/media/) and converts it into a CIDOC CRM RDF Graph (hopefully) validating against the (in)famous [PFP-Shacl](https://pfp-schema.acdh-ch-dev.oeaw.ac.at/shacl/shacl.ttl).

## pfp
If you don't know what PFP stands for: [PFP](https://www.oeaw.ac.at/acdh/research/dh-research-infrastructure/activities/modelling-humanities-data/pfp-prosopographical-research-platform-austria) means **Prosopographical Research Platform Austria** and yes, it only makes sense in the German translation **Prosopographische Forschungsplattform Österreich**.


## develop


```bash
git clone https://github.com/arthur-schnitzler/pmb2pfp.git
cd pmb2pfp
[python -m venv venv]
[source venv/bin/activate]
pip install -r requirements.txt
cp .env .secret [and add your ownloud credentials]
```



## build the graph and upload it to ownlcoud
```bash
./scripts/build_pmb_graph.sh
```

the graph is uploaded to [owncloud](https://cloud.oeaw.ac.at/index.php/s/NTjXBotgP988rbB)


## validate

```bash
./validate.sh
```

## convert nt to ttl
```bash
./convert.sh
```