"""Shared PostgreSQL settings from database.ini for psycopg2.connect."""

from configparser import ConfigParser

DEFAULT_SCHEMA = "public"


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
