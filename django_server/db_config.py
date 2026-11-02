"""Shared PostgreSQL settings from database.ini for psycopg2.connect."""

import os
from configparser import ConfigParser
from os import path

DEFAULT_SCHEMA = "public"


def project_root():
    """Repository root (parent of the django_server package)."""
    return path.abspath(path.join(path.dirname(__file__), os.pardir))


def database_ini_path():
    """
    Production gunicorn keeps cwd /home/alexb, where database.ini already exists.
    CHEMMAPS_DB_CONFIG selects another file. Otherwise use ./database.ini when
    that file exists, then the copy next to the repository.
    """
    env = os.environ.get("CHEMMAPS_DB_CONFIG")
    if env:
        return path.abspath(env)
    cwd_ini = path.abspath("./database.ini")
    if path.isfile(cwd_ini):
        return cwd_ini
    return path.join(project_root(), "database.ini")


def temp_root():
    """Session upload directory. CHEMMAPS_TEMP overrides the cwd ./temp default."""
    env = os.environ.get("CHEMMAPS_TEMP")
    if env:
        return path.abspath(env)
    return path.abspath("./temp")


def load_postgresql_settings(config_path):
    """
    Returns (connect_kwargs, schema_name) suitable for psycopg2.connect(**connect_kwargs).
    Maps legacy ``database`` ini key to psycopg2 ``dbname``.
    """
    parser = ConfigParser()
    read_ok = parser.read(config_path)
    if not read_ok:
        raise Exception("Could not read database config file: %s" % config_path)
    if not parser.has_section("postgresql"):
        raise Exception(
            "Section postgresql not found in {0}".format(config_path)
        )

    opts = {k.lower(): v for k, v in parser.items("postgresql")}
    schema = opts.pop("schema", DEFAULT_SCHEMA)
    dbname = opts.pop("dbname", None) or opts.pop("database", None)
    opts.pop("database", None)
    opts.pop("dbname", None)
    if not dbname:
        raise Exception(
            "postgresql.dbname or database must be set in {0}".format(config_path)
        )

    connect = dict(opts)
    connect["dbname"] = dbname
    if "port" in connect:
        connect["port"] = int(str(connect["port"]))
    connect["options"] = "-c search_path=dbo,%s" % schema
    return connect, schema
