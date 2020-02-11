"""Create the projects.json file that can be served from S3 via API Gateway. This
is used to create a mock endpoint for the browser to use during development.
"""

import json
import requests

AZUL_URL = "https://service.explore.data.humancellatlas.org/repository/projects?size=50"

resp = requests.get(AZUL_URL).json()

projects = []

id_ = 1
for hit in sorted(resp["hits"], key=lambda h: h["projects"][0]["projectShortname"]):

    # Don't include test projects (or whatever these are)
    if hit["projects"][0]["projectShortname"].startswith("prod/"):
        continue

    assays = set()
    for prot in hit["protocols"]:
        for assay in prot["libraryConstructionApproach"]:
            assays.add(assay)

    specieses = set()
    for donor in hit["donorOrganisms"]:
        for species in donor["genusSpecies"]:
            specieses.add(species)

    organs = set()
    for sample in hit["samples"]:
        for organ in sample["effectiveOrgan"]:
            organs.add(organ)

    total_cells = sum(c["totalCells"] for c in hit["cellSuspensions"])
    total_file_size = sum(f["totalSize"] for f in hit["fileTypeSummaries"])

    projects.append(
        {
            "short_name": hit["projects"][0]["projectShortname"],
            "title": hit["projects"][0]["projectTitle"],
            "assays": list(sorted(assays)),
            "species": list(sorted(specieses)),
            "organs": list(sorted(organs)),
            "total_cells": total_cells,
            "total_file_size": total_file_size,
            "id": str(id_)
        }
    )
    id_ += 1

print(json.dumps(projects))
