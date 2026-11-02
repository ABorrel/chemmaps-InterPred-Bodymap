import re

import psycopg2

from django_server.db_config import database_ini_path, load_postgresql_settings


_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_COLUMN_LIST = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(?:\[\d+\])?(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*(?:\[\d+\])?)*$"
)
# Condition text is fixed SQL from this app, plus %s placeholders. No quotes.
_CONDITION = re.compile(r"^[A-Za-z0-9_ %=<>!()\s]*$")

ALLOWED_TABLES = frozenset(
    {
        "chemicals",
        "chemicals_user",
        "chem_descriptor_1d2d_name",
        "chem_descriptor_3d_name",
        "chem_descriptor_opera_name",
        "chem_prop_drugbank_name",
        "chem_toxexp_name",
        "chemical_description",
        "chemical_description_user",
        "mvwchemmap_mapdrugbank",
        "mvwchemmap_mappfas",
        "mvwchemmap_maptox21",
        "mvwchemmap_mapdsstox",
    }
)

ALLOWED_COLUMNS = frozenset(
    {
        "name",
        "smiles_clean",
        "smiles_origin",
        "inchikey",
        "dsstox_id",
        "drugbank_id",
        "status",
        "desc_1d2d",
        "desc_3d",
        "source_id",
        "map_name",
        "dim1d2d",
        "dim3d",
        "d3_cube",
        "neighbors_dim3",
        "prop_value",
        "prop_tox",
    }
)


def quote_ident(name):
    if not isinstance(name, str) or not _IDENT.match(name):
        raise ValueError("identifier rejected")
    return name


def quote_table(name):
    if name not in ALLOWED_TABLES:
        raise ValueError("table rejected")
    return quote_ident(name)


def quote_columns(spec):
    if isinstance(spec, (list, tuple)):
        spec = ", ".join(spec)
    spec = spec.strip()
    if not _COLUMN_LIST.match(spec):
        raise ValueError("column list rejected")
    for part in spec.split(","):
        base = part.strip().split("[", 1)[0]
        if base not in ALLOWED_COLUMNS:
            raise ValueError("column rejected")
    return ", ".join(part.strip() for part in spec.split(","))


def check_condition(condition):
    condition = (condition or "").strip()
    if condition and not _CONDITION.match(condition):
        raise ValueError("condition rejected")
    return condition


class DBrequest:
    def __init__(self, verbose=1):
        self.dbconfig = database_ini_path()
        self.conn = None
        self.verbose = verbose
        self.connect_kwargs = None
        self.schema = None

    def config(self, section="postgresql"):
        del section
        self.connect_kwargs, self.schema = load_postgresql_settings(self.dbconfig)
        self.params = dict(self.connect_kwargs)
        quote_ident(self.schema)

    def relation(self, table):
        """schema.table, both identifiers, neither taken from the request."""
        if not self.schema:
            self.config()
        return "%s.%s" % (quote_ident(self.schema), quote_table(table))

    def connOpen(self):
        try:
            self.config()
            if self.verbose:
                print("Connecting to the PostgreSQL database...")
            if self.conn is not None:
                return
            self.conn = psycopg2.connect(**self.connect_kwargs)
        except (Exception, psycopg2.DatabaseError):
            self.conn = None

    def connClose(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            if self.verbose == 1:
                print("Database connection closed.")

    def _execute(self, cur, sqlCMD, params):
        if params:
            cur.execute(sqlCMD, params)
        else:
            cur.execute(sqlCMD)

    def addElement(self, nameTable, lcoloumn, lval):
        self.connOpen()
        try:
            sqlCMD = "INSERT INTO %s(%s) VALUES(%s);" % (
                quote_table(nameTable),
                quote_columns(lcoloumn),
                ",".join(["%s"] * len(lval)),
            )
        except ValueError:
            self.connClose()
            return
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(sqlCMD, list(lval))
                self.conn.commit()
                self.connClose()
            except (Exception, psycopg2.DatabaseError):
                self.connClose()
        else:
            print("Open connection first")

    def extractColoumn(self, nameTable, coloumn, condition="", params=None, close_conn=True):
        """Fetch rows. Values belong in params, never inside condition."""
        self.verbose = 0
        self.connOpen()
        try:
            sqlCMD = "SELECT %s FROM %s %s;" % (
                quote_columns(coloumn),
                quote_table(nameTable),
                check_condition(condition),
            )
        except ValueError:
            if close_conn:
                self.connClose()
            return "ERROR"
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                self._execute(cur, sqlCMD, params)
                return cur.fetchall()
            except (Exception, psycopg2.DatabaseError):
                return "ERROR"
            finally:
                if close_conn:
                    self.connClose()
        else:
            print("Open connection first")
            if close_conn:
                self.connClose()
            return "ERROR"

    def getRow(self, table, condition, params=None):
        self.connOpen()
        try:
            sqlCMD = "SELECT * FROM %s WHERE %s;" % (
                quote_table(table),
                check_condition(condition),
            )
        except ValueError:
            self.connClose()
            return "ERROR"
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                self._execute(cur, sqlCMD, params)
                out = cur.fetchall()
                self.connClose()
                return out
            except (Exception, psycopg2.DatabaseError):
                self.connClose()
                return "ERROR"
        else:
            self.connClose()
            print("Open connection first")
            return "ERROR"

    def execCMD(self, cmdSQL, params=None):
        out = None
        self.connOpen()
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                self._execute(cur, cmdSQL, params)
                out = cur.fetchall()
            except (Exception, psycopg2.DatabaseError):
                self.connClose()
                return "Error"
        else:
            print("Open connection first")
            return "Error"
        self.connClose()
        return out

    def updateElement(self, cmdSQL, params=None):
        self.connOpen()
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                self._execute(cur, cmdSQL, params)
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError):
                self.connClose()
                return "Error"
        else:
            print("Open connection first")
        self.connClose()
        return 0
