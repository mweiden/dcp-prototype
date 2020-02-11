"""Create the set of project detail json files that can used to mock
an endpoint for the browser.

Assumes you've already created the "projects.json" file and got a download
manifest from the DCP/1 data browser.
"""

import csv
import enum
import json
import os
import sys
import uuid


class FileType(enum.Enum):
    FASTQ = 'fastq'
    BAM = 'bam'
    MATRIX = 'matrix'

project_list = json.load(open("projects.json"))
project_name_to_id = {p["short_name"]: p["id"] for p in project_list}

files = {}

with open("download_manifest.tsv", encoding='utf-8') as project_tsv_file:
    reader = csv.DictReader(project_tsv_file, delimiter='\t')
    for row in reader:
        file_name = row["file_name"]
        file_size = int(row["file_size"])

        project_name = row["project.project_core.project_short_name"]
        project_id = project_name_to_id[project_name]
        species = row["donor_organism.genus_species"]
        assay = row["library_preparation_protocol.library_construction_approach"]

        if row["organoid.model_organ"]:
            organ = row["organoid.model_organ"] + " (organoid)"
        else:
            organ = row["specimen_from_organism.organ"]

        if file_name.endswith('.bam'):
            file_type = FileType.BAM
        elif file_name.endswith('.npz'):
            file_type = FileType.MATRIX
        elif 'fastq' in file_name or 'fq' in file_name:
            file_type = FileType.FASTQ
        else:
            continue

        key = (project_id, project_name, species, assay, organ, file_type.value)

        current_counts = files.get(key, (0, 0))

        files[key] = (current_counts[0] + 1, current_counts[1] + file_size)

keys = list(files.keys())
project_ids = set(k[0] for k in keys)
for project_id in project_ids:
    project_keys = [k for k in keys if k[0] == project_id]

    project_file_objs = []

    for key in project_keys:
        project_id, project_name, species, assay, organ, type_ = key
        count, size = files[key]
        file_name = type_ + '.zip'

        project_file_objs.append({
            "project_id": project_id,
            "species": species,
            "assay": assay,
            "organ": organ,
            "file_type": type_,
            "file_name": file_name,
            "file_count": count,
            "file_size": size,
            "file_key": str(uuid.uuid4())
        })
    json.dump({"files": project_file_objs}, open(project_id, 'w'))
