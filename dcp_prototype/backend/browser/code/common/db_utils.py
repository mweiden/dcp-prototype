import os
import sys

from sqlalchemy import or_

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from browser.code.common.browser_orm import (
    DBSessionMaker,
    File,
    LibraryPrepProtocol,
    Tissue,
    Species,
    LibraryPrepProtocolJoinProject,
    TissueJoinProject,
    SpeciesJoinProject,
)


def get_project_assays(project_id, session=None):
    """
    Query the DB to return all assays that are represented in a given project.
    :param project_id: Project to return assays for
    :param session: SQLAlchemy DBSession
    :return: list of assay ontology IDs
    """
    if not session:
        session = DBSessionMaker().session()

    assays = []
    for result in (
        session.query(LibraryPrepProtocolJoinProject, LibraryPrepProtocol)
        .filter(
            (LibraryPrepProtocolJoinProject.library_prep_protocol_id == LibraryPrepProtocol.id),
            LibraryPrepProtocolJoinProject.project_id == project_id,
        )
        .all()
    ):
        assays.append(result.LibraryPrepProtocol.construction_method_ontology)

    return assays


def get_project_tissues(project_id, session=None):
    """
    Query the DB to return all tissues that are represented in a given project.
    :param project_id: Project to return tissues for
    :param session: SQLAlchemy DBSession
    :return: list of tissue ontology IDs
    """
    if not session:
        session = DBSessionMaker().session()

    tissues = []
    for result in (
        session.query(TissueJoinProject, Tissue)
        .filter(TissueJoinProject.tissue_id == Tissue.id, TissueJoinProject.project_id == project_id,)
        .all()
    ):
        tissues.append(result.Tissue.tissue_ontology)

    return tissues


def get_project_species(project_id, session=None):
    """
    Query the DB to return all species that are represented in a given project.
    :param project_id: Project to return species for
    :param session: SQLAlchemy DBSession
    :return: list of species labels
    """
    if not session:
        session = DBSessionMaker().session()

    species = []
    for result in (
        session.query(SpeciesJoinProject, Species)
        .filter(SpeciesJoinProject.species_id == Species.id, SpeciesJoinProject.project_id == project_id,)
        .all()
    ):
        species.append(result.Species.species_ontology)

    return species


def get_downloadable_project_files(project_id, session=None):
    """
    Query the DB to return all downloadable files for a project.
    :param project_id: Project to return files for
    :param session: SQLAlchemy DBSession
    :return: list of file metadata objects
    """
    files = []
    for file in (session.query(File)
                        .filter(File.project_id == project_id)
                        .filter(or_(File.file_format == "loom",
                                    File.file_format == "csv.gz",
                                    File.file_format == "mtx.gz",
                                    File.file_format == "gz"))):
        files.append(
            {
                "id": file.id,
                "filename": file.filename,
                "file_format": file.file_format,
                "file_size": file.file_size,
                "species": file.species,
                "library_construction_method_ontology": file.library_construction_method_ontology,
                "tissue_ontology": file.tissue_ontology,
            }
        )

    return files
