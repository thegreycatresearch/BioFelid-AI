import requests


NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


FELIDAE_SPECIES = [
    {
        "taxid": 32536,
        "scientific_name": "Acinonyx jubatus",
        "conservation_status": "VU",
    },
    {
        "taxid": 3369756,
        "scientific_name": "Caracal auratus",
        "conservation_status": "VU",
    },
    {
        "taxid": 61394,
        "scientific_name": "Caracal caracal",
        "conservation_status": "LC",
    },
    {
        "taxid": 61454,
        "scientific_name": "Catopuma badia",
        "conservation_status": "EN",
    },
    {
        "taxid": 61455,
        "scientific_name": "Catopuma temminckii",
        "conservation_status": "NT",
    },
    {
        "taxid": 9685,
        "scientific_name": "Felis catus",
        "conservation_status": "LC",
    },
    {
        "taxid": 61376,
        "scientific_name": "Felis chaus",
        "conservation_status": "LC",
    },
    {
        "taxid": 61378,
        "scientific_name": "Felis margarita",
        "conservation_status": "LC",
    },
    {
        "taxid": 61379,
        "scientific_name": "Felis nigripes",
        "conservation_status": "VU",
    },
    {
        "taxid": 9683,
        "scientific_name": "Felis silvestris",
        "conservation_status": "LC",
    },
    {
        "taxid": 1608482,
        "scientific_name": "Herpailurus yagouaroundi",
        "conservation_status": "LC",
    },

    # Extinct prehistoric felids
    {
        "taxid": 2048657,
        "scientific_name": "Homotherium latidens",
        "conservation_status": "EX",
    },
    {
        "taxid": 339614,
        "scientific_name": "Homotherium serum",
        "conservation_status": "EX",
    },

    {
        "taxid": 3055696,
        "scientific_name": "Leopardus colocola",
        "conservation_status": "NT",
    },
    {
        "taxid": 3370150,
        "scientific_name": "Leopardus fasciatus",
        "conservation_status": "DD",
    },
    {
        "taxid": 46844,
        "scientific_name": "Leopardus geoffroyi",
        "conservation_status": "LC",
    },
    {
        "taxid": 61386,
        "scientific_name": "Leopardus guigna",
        "conservation_status": "VU",
    },
    {
        "taxid": 1608501,
        "scientific_name": "Leopardus guttulus",
        "conservation_status": "VU",
    },
    {
        "taxid": 713925,
        "scientific_name": "Leopardus jacobita",
        "conservation_status": "EN",
    },
    {
        "taxid": 32538,
        "scientific_name": "Leopardus pardalis",
        "conservation_status": "LC",
    },
    {
        "taxid": 3370154,
        "scientific_name": "Leopardus pardinoides",
        "conservation_status": "VU",
    },
    {
        "taxid": 46842,
        "scientific_name": "Leopardus tigrinus",
        "conservation_status": "VU",
    },
    {
        "taxid": 61382,
        "scientific_name": "Leopardus wiedii",
        "conservation_status": "NT",
    },
    {
        "taxid": 61405,
        "scientific_name": "Leptailurus serval",
        "conservation_status": "LC",
    },

    {
        "taxid": 61383,
        "scientific_name": "Lynx canadensis",
        "conservation_status": "LC",
    },
    {
        "taxid": 13125,
        "scientific_name": "Lynx lynx",
        "conservation_status": "LC",
    },
    {
        "taxid": 191816,
        "scientific_name": "Lynx pardinus",
        "conservation_status": "VU",
    },
    {
        "taxid": 61384,
        "scientific_name": "Lynx rufus",
        "conservation_status": "LC",
    },

    # Extinct cheetah relative
    {
        "taxid": 339612,
        "scientific_name": "Miracinonyx trumani",
        "conservation_status": "EX",
    },

    {
        "taxid": 427616,
        "scientific_name": "Neofelis diardi",
        "conservation_status": "VU",
    },
    {
        "taxid": 61452,
        "scientific_name": "Neofelis nebulosa",
        "conservation_status": "VU",
    },
    {
        "taxid": 61408,
        "scientific_name": "Otocolobus manul",
        "conservation_status": "NT",
    },

    {
        "taxid": 9689,
        "scientific_name": "Panthera leo",
        "conservation_status": "VU",
    },
    {
        "taxid": 9690,
        "scientific_name": "Panthera onca",
        "conservation_status": "NT",
    },
    {
        "taxid": 9691,
        "scientific_name": "Panthera pardus",
        "conservation_status": "VU",
    },
    {
        "taxid": 2770979,
        "scientific_name": "Panthera spelaea",
        "conservation_status": "EX",
    },
    {
        "taxid": 9694,
        "scientific_name": "Panthera tigris",
        "conservation_status": "EN",
    },
    {
        "taxid": 29064,
        "scientific_name": "Panthera uncia",
        "conservation_status": "VU",
    },

    {
        "taxid": 61410,
        "scientific_name": "Pardofelis marmorata",
        "conservation_status": "VU",
    },

    {
        "taxid": 37029,
        "scientific_name": "Prionailurus bengalensis",
        "conservation_status": "LC",
    },
    {
        "taxid": 37030,
        "scientific_name": "Prionailurus iriomotensis",
        "conservation_status": "DD",
    },
    {
        "taxid": 61403,
        "scientific_name": "Prionailurus planiceps",
        "conservation_status": "EN",
    },
    {
        "taxid": 61387,
        "scientific_name": "Prionailurus rubiginosus",
        "conservation_status": "VU",
    },
    {
        "taxid": 61388,
        "scientific_name": "Prionailurus viverrinus",
        "conservation_status": "VU",
    },

    {
        "taxid": 9696,
        "scientific_name": "Puma concolor",
        "conservation_status": "LC",
    },

    # Extinct Smilodon
    {
        "taxid": 13266,
        "scientific_name": "Smilodon fatalis",
        "conservation_status": "EX",
    },
    {
        "taxid": 339609,
        "scientific_name": "Smilodon populator",
        "conservation_status": "EX",
    },
]

def search_felidae_taxa():
    params = {
        "db": "taxonomy",
        "term": "Felidae[Organism]",
        "retmode": "json",
        "retmax": 500,
    }

    response = requests.get(
        f"{NCBI_BASE_URL}esearch.fcgi",
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    return data["esearchresult"]["idlist"]


def get_taxonomy_records(taxids):
    if not taxids:
        return []

    params = {
        "db": "taxonomy",
        "id": ",".join(taxids),
        "retmode": "json",
    }

    response = requests.get(
        f"{NCBI_BASE_URL}esummary.fcgi",
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    return [
        data["result"][taxid]
        for taxid in taxids
        if taxid in data["result"]
    ]

def get_conservation_status(taxid):
    for species in FELIDAE_SPECIES:
        if species["taxid"] == taxid:
            return species["conservation_status"]

    return "DD"

def get_felidae_species():
    taxids = search_felidae_taxa()
    records = get_taxonomy_records(taxids)

    species = []

    for record in records:
        scientific_name = record.get("scientificname")
        rank = record.get("rank")

        if not scientific_name:
            continue

        if rank != "species":
            continue

        # Exclude unresolved or non-standard taxa
        if " sp." in scientific_name:
            continue

        if "environmental sample" in scientific_name.lower():
            continue

        # Exclude hybrid names
        if " x " in scientific_name:
            continue

        species.append(
    {
        "taxid": int(record["taxid"]),
        "scientific_name": scientific_name,
        "conservation_status": get_conservation_status(
            int(record["taxid"])
        ),
    }
)

    species.sort(key=lambda item: item["scientific_name"])

    return species


if __name__ == "__main__":
    results = get_felidae_species()

    print(f"Found {len(results)} Felidae taxa")

    for species in results[:20]:
        print(species)