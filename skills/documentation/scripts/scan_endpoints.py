#!/usr/bin/env python3
"""
scan_endpoints.py - Varre um projeto Python, encontra todos os endpoints HTTP
expostos e mapeia, para cada um, as fronteiras (sistemas externos) que ele toca.

Fronteiras = outra API/ACL, banco de dados, cache, fila, storage, e-mail, etc.
Objetos e classes internas NAO sao mapeados de proposito: o objetivo e enxergar
o que sai do processo.

Saida: um JSON de inventario (stdout ou --out) consumido por generate_mermaid.py.

Uso:
    python scan_endpoints.py /caminho/do/projeto --out inventory.json
    python scan_endpoints.py . --app-name "Minha API" --include-consumers

Sem dependencias externas: usa somente a stdlib (ast).
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Configuracao de varredura
# --------------------------------------------------------------------------

DEFAULT_EXCLUDES = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", ".env", "node_modules",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    "site-packages", "dist", "build", ".eggs", "migrations", ".idea", ".vscode",
    "htmlcov", ".next", "static", "docs",
}

TEST_HINTS = re.compile(r"(^|/)(tests?|testing)(/|$)|(^|/)(test_[^/]+|[^/]+_test)\.py$")

MAX_DEPTH = 8  # profundidade maxima ao seguir a cadeia de chamadas

# --------------------------------------------------------------------------
# Catalogo de fronteiras
#
# Cada regra casa por: modulos importados (roots), nome de variavel do objeto
# (var_re) e metodo chamado (attrs). A ordem importa - regras mais especificas
# primeiro, porque `.get(` pode ser Redis, HTTP ou um dicionario.
# --------------------------------------------------------------------------

SQL_VERB_BY_METHOD = {
    "filter": "SELECT", "filter_by": "SELECT", "get": "SELECT", "all": "SELECT",
    "first": "SELECT", "one": "SELECT", "one_or_none": "SELECT", "count": "SELECT",
    "exists": "SELECT", "scalar": "SELECT", "scalars": "SELECT", "query": "SELECT",
    "select": "SELECT", "fetch": "SELECT", "fetchall": "SELECT", "fetchone": "SELECT",
    "fetchrow": "SELECT", "fetchval": "SELECT", "find": "SELECT", "read": "SELECT",
    "list": "SELECT", "aggregate": "SELECT",
    "add": "INSERT", "add_all": "INSERT", "create": "INSERT", "insert": "INSERT",
    "bulk_create": "INSERT", "bulk_save_objects": "INSERT", "save": "UPSERT",
    "update": "UPDATE", "bulk_update": "UPDATE", "merge": "UPDATE",
    "delete": "DELETE", "remove": "DELETE",
    "commit": "COMMIT", "flush": "FLUSH", "rollback": "ROLLBACK",
    "execute": "EXECUTE", "executemany": "EXECUTE", "exec_driver_sql": "EXECUTE",
    "refresh": "SELECT",
}

REDIS_ATTRS = {
    "get", "mget", "set", "mset", "setex", "setnx", "psetex", "getset", "append",
    "incr", "incrby", "decr", "decrby", "expire", "expireat", "ttl", "persist",
    "delete", "unlink", "exists", "keys", "scan", "hget", "hgetall", "hset",
    "hmset", "hmget", "hdel", "hincrby", "lpush", "rpush", "lpop", "rpop",
    "lrange", "llen", "sadd", "srem", "smembers", "sismember", "zadd", "zrange",
    "zrem", "zscore", "publish", "subscribe", "setbit", "getbit", "pipeline",
    "flushdb", "cache_get", "cache_set",
}

HTTP_ATTRS = {"get", "post", "put", "patch", "delete", "head", "options",
              "request", "send", "stream", "fetch", "urlopen", "call"}

RULES = [
    # ---- filas / mensageria -------------------------------------------------
    dict(system="RabbitMQ", kind="queue",
         roots={"pika", "aio_pika", "aiormq", "kombu", "amqpstorm", "amqp"},
         var_re=r"(channel|rabbit|amqp|publisher|producer|broker|exchange|queue)",
         attrs={"basic_publish", "publish", "send", "send_message", "basic_consume",
                "declare_queue", "declare_exchange", "queue_declare", "exchange_declare",
                "basic_get", "consume"}),
    dict(system="Kafka", kind="queue",
         roots={"kafka", "aiokafka", "confluent_kafka", "faust"},
         var_re=r"(kafka|producer|consumer)",
         attrs={"send", "send_and_wait", "produce", "poll", "flush", "consume",
                "subscribe", "start", "stop"}),
    dict(system="SQS", kind="queue",
         roots={"boto3", "aioboto3", "botocore"},
         var_re=r"(sqs|queue)",
         attrs={"send_message", "send_message_batch", "receive_message",
                "delete_message", "change_message_visibility"}),
    dict(system="Celery", kind="queue",
         roots={"celery"}, var_re=r"(celery|task|worker)",
         attrs={"delay", "apply_async", "send_task", "apply"}),

    # ---- cache --------------------------------------------------------------
    dict(system="Redis", kind="cache",
         roots={"redis", "aioredis", "redis.asyncio", "fakeredis", "walrus"},
         var_re=r"(redis|cache|kv_store|kvstore)",
         attrs=REDIS_ATTRS),
    dict(system="Memcached", kind="cache",
         roots={"pymemcache", "memcache", "aiomcache"},
         var_re=r"(memcache|mc_client)",
         attrs={"get", "set", "add", "delete", "incr", "decr", "get_multi"}),

    # ---- bancos NoSQL / busca ----------------------------------------------
    dict(system="MongoDB", kind="database",
         roots={"pymongo", "motor", "mongoengine", "beanie", "bson"},
         var_re=r"(mongo|collection|db\b|documents?)",
         attrs={"find", "find_one", "find_one_and_update", "insert_one",
                "insert_many", "update_one", "update_many", "delete_one",
                "delete_many", "replace_one", "count_documents", "aggregate",
                "bulk_write"}),
    dict(system="Elasticsearch", kind="database",
         roots={"elasticsearch", "opensearchpy", "elastic_transport"},
         var_re=r"(elastic|opensearch|es_client|search_client)",
         attrs={"search", "index", "get", "delete", "bulk", "update", "msearch",
                "count", "indices"}),
    dict(system="DynamoDB", kind="database",
         roots={"boto3", "aioboto3"}, var_re=r"(dynamo|table)",
         attrs={"put_item", "get_item", "query", "scan", "update_item",
                "delete_item", "batch_write_item"}),

    # ---- storage / arquivos -------------------------------------------------
    dict(system="S3", kind="storage",
         roots={"boto3", "aioboto3", "botocore", "minio"},
         var_re=r"(s3|bucket|storage|minio|blob)",
         attrs={"put_object", "get_object", "upload_file", "upload_fileobj",
                "download_file", "download_fileobj", "delete_object",
                "list_objects", "list_objects_v2", "generate_presigned_url",
                "copy_object", "head_object", "fput_object", "fget_object"}),

    # ---- e-mail / notificacao ----------------------------------------------
    dict(system="SMTP", kind="external_api",
         roots={"smtplib", "email", "emails", "sendgrid", "mailgun", "ses",
                "postmarker", "mailjet"},
         var_re=r"(smtp|mail|sendgrid|mailer|message|msg)",
         attrs={"send_message", "sendmail", "send", "send_mail"}),

    # ---- bancos relacionais -------------------------------------------------
    dict(system="__SQL__", kind="database",
         roots={"sqlalchemy", "psycopg2", "psycopg", "asyncpg", "pymysql",
                "aiomysql", "mysql", "sqlite3", "aiosqlite", "sqlmodel",
                "databases", "tortoise", "peewee", "pyodbc", "cx_Oracle",
                "oracledb", "django"},
         var_re=r"(session|conn|connection|cur|cursor|engine|db|database|repository|repo|dao|objects|pool|tx|transaction)",
         attrs=set(SQL_VERB_BY_METHOD)),

    # ---- chamadas HTTP para fora (ACL / outra API) --------------------------
    dict(system="__HTTP__", kind="external_api",
         roots={"requests", "httpx", "aiohttp", "urllib", "urllib3", "http",
                "grpc", "zeep", "suds", "requests_oauthlib"},
         var_re=r"(client|session|http|api|gateway|acl|integration|adapter|connector|service_client|proxy|caller)",
         attrs=HTTP_ATTRS),
]

# dialeto SQL a partir do import
SQL_FLAVOR = [
    (re.compile(r"^(psycopg2?|asyncpg)\b"), "PostgreSQL"),
    (re.compile(r"^(pymysql|aiomysql|MySQLdb|mysql)\b"), "MySQL"),
    (re.compile(r"^(sqlite3|aiosqlite)\b"), "SQLite"),
    (re.compile(r"^(pyodbc)\b"), "SQL Server"),
    (re.compile(r"^(cx_Oracle|oracledb)\b"), "Oracle"),
]
URL_FLAVOR = [
    (re.compile(r"postgres(ql)?(\+\w+)?://", re.I), "PostgreSQL"),
    (re.compile(r"mysql(\+\w+)?://", re.I), "MySQL"),
    (re.compile(r"sqlite(\+\w+)?://", re.I), "SQLite"),
    (re.compile(r"mssql(\+\w+)?://", re.I), "SQL Server"),
    (re.compile(r"oracle(\+\w+)?://", re.I), "Oracle"),
    (re.compile(r"django\.db\.backends\.postgresql", re.I), "PostgreSQL"),
    (re.compile(r"django\.db\.backends\.mysql", re.I), "MySQL"),
    (re.compile(r"django\.db\.backends\.sqlite3", re.I), "SQLite"),
]

# pistas fracas no codigo-fonte (contadas por ocorrencia, vence a mais citada)
SRC_HINTS = [
    (re.compile(r"postgres|psycopg|asyncpg|pgbouncer", re.I), "PostgreSQL"),
    (re.compile(r"\bmysql|pymysql|aiomysql|mariadb", re.I), "MySQL"),
    (re.compile(r"\bsqlite", re.I), "SQLite"),
    (re.compile(r"\bmssql|pyodbc|sqlserver", re.I), "SQL Server"),
    (re.compile(r"\boracle|cx_Oracle|oracledb", re.I), "Oracle"),
]

ROUTE_DECOS = {"get", "post", "put", "patch", "delete", "head", "options",
               "route", "websocket", "api_route"}

CONSUMER_HINTS = re.compile(
    r"(basic_consume|@app\.task|@shared_task|@celery|consume\(|start_consuming|"
    r"@router\.subscriber|KafkaConsumer|@app\.agent)")


# --------------------------------------------------------------------------
# Construtores: `x = redis.Redis()` diz muito mais sobre `x.get(...)` do que o
# nome do metodo sozinho. O coletor abaixo tipa as variaveis antes da varredura
# principal, o que elimina a maior parte dos falsos positivos/negativos.
# --------------------------------------------------------------------------

BOTO_SERVICES = {"s3": ("S3", "storage"), "sqs": ("SQS", "queue"),
                 "dynamodb": ("DynamoDB", "database"), "ses": ("SMTP", "external_api"),
                 "sns": ("SNS", "queue"), "kinesis": ("Kinesis", "queue"),
                 "secretsmanager": ("SecretsManager", "external_api")}

CTORS = [
    ({"Redis", "StrictRedis", "ConnectionPool"}, {"redis", "aioredis", "fakeredis"},
     "Redis", "cache"),
    ({"BlockingConnection", "SelectConnection", "connect_robust", "Connection"},
     {"pika", "aio_pika", "aiormq", "kombu"}, "RabbitMQ", "queue"),
    ({"KafkaProducer", "KafkaConsumer", "AIOKafkaProducer", "AIOKafkaConsumer",
      "Producer", "Consumer"}, {"kafka", "aiokafka", "confluent_kafka"},
     "Kafka", "queue"),
    ({"MongoClient", "AsyncIOMotorClient"}, {"pymongo", "motor"}, "MongoDB", "database"),
    ({"Elasticsearch", "AsyncElasticsearch", "OpenSearch"},
     {"elasticsearch", "opensearchpy"}, "Elasticsearch", "database"),
    ({"Minio"}, {"minio"}, "S3", "storage"),
    ({"SMTP", "SMTP_SSL"}, {"smtplib"}, "SMTP", "external_api"),
    ({"connect", "create_pool", "create_engine", "sessionmaker", "scoped_session",
      "Session", "AsyncSession", "SessionLocal", "async_sessionmaker"},
     {"sqlalchemy", "psycopg2", "psycopg", "asyncpg", "pymysql", "aiomysql",
      "sqlite3", "aiosqlite", "sqlmodel", "databases", "mysql"}, "__SQL__", "database"),
    ({"Client", "AsyncClient", "ClientSession", "Session", "PoolManager"},
     {"httpx", "requests", "aiohttp", "urllib3"}, "__HTTP__", "external_api"),
]

# metodos plausiveis por sistema, usados quando a variavel ja esta tipada
# (preenchido logo apos a definicao de RULES)
SYSTEM_ATTRS = {}

for _r in RULES:
    SYSTEM_ATTRS.setdefault(_r["system"], set()).update(_r["attrs"])
SYSTEM_ATTRS["__SQL__"].update({"begin", "close", "acquire", "transaction"})
SYSTEM_ATTRS["__HTTP__"].update({"get_json", "post_json"})
for _sys, _kind in BOTO_SERVICES.values():
    SYSTEM_ATTRS.setdefault(_sys, set()).update(
        {"publish", "send_message", "put_object", "get_object", "put_item",
         "get_item", "query", "scan", "send_email"})



class VarTypeCollector(ast.NodeVisitor):
    """Descobre `var -> sistema` a partir de construtores e heranca de atributo."""

    def __init__(self, imports, var_types, label_hints):
        self.imports = imports
        self.var_types = var_types
        self.labels = label_hints

    def visit_Assign(self, node):
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if not targets:
            self.generic_visit(node)
            return
        info = self.classify(node.value)
        if info:
            system, kind, label = info
            for t in targets:
                self.var_types[t] = (system, kind)
                if label:
                    self.labels[t] = label
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name) and node.value is not None:
            info = self.classify(node.value)
            if info:
                self.var_types[node.target.id] = (info[0], info[1])
        self.generic_visit(node)

    def classify(self, value):
        if isinstance(value, ast.Await):
            value = value.value
        if isinstance(value, (ast.Attribute, ast.Subscript)) and not isinstance(value, ast.Call):
            root = dotted(value).split(".")[0]
            if root in self.var_types:
                s, k = self.var_types[root]
                return (s, k, None)
            return None
        if not isinstance(value, ast.Call):
            return None
        name = dotted(value.func)
        if not name:
            return None
        parts = name.split(".")
        tail, root = parts[-1], parts[0]
        root_mod = self.imports.get(root, root)

        # boto3.client("s3") / resource("sqs")
        if tail in {"client", "resource"} and ("boto" in root_mod or "boto" in name):
            svc = const_str(value.args[0]) if value.args else None
            if svc and svc.lower() in BOTO_SERVICES:
                sysname, kind = BOTO_SERVICES[svc.lower()]
                return (sysname, kind, None)

        # Django ORM: order = Order.objects.get(...) -> a instancia fala com o banco
        if ".objects." in name:
            return ("__SQL__", "database", None)

        # metodo em cima de variavel ja tipada: conn.cursor(), connection.channel()
        if root in self.var_types and tail in {
                "cursor", "channel", "connect", "begin", "get_session", "session",
                "acquire", "pipeline", "get_database", "get_collection", "client"}:
            s, k = self.var_types[root]
            return (s, k, self.labels.get(root))

        for tails, roots, system, kind in CTORS:
            if tail not in tails:
                continue
            if any(root_mod == r or root_mod.startswith(r + ".") or
                   re.search(rf"(^|\.){re.escape(r)}(\.|$)", name.lower())
                   for r in roots):
                label = None
                if system == "__HTTP__":
                    label = kwarg_str(value, "base_url") or kwarg_str(value, "url")
                return (system, kind, label)
        return None


# --------------------------------------------------------------------------
# Utilitarios de AST
# --------------------------------------------------------------------------

def dotted(node):
    """Transforma uma expressao em string pontuada: a.b.c(...) -> 'a.b.c'."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return dotted(node.func)
    if isinstance(node, ast.Subscript):
        return dotted(node.value)
    if isinstance(node, ast.Await):
        return dotted(node.value)
    return ""


def const_str(node):
    """Extrai string literal (inclusive f-string com partes literais)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        out = []
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                out.append(v.value)
            else:
                out.append("{...}")
        return "".join(out)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = const_str(node.left), const_str(node.right)
        if left or right:
            return f"{left or '{...}'}{right or '{...}'}"
    return None


def kwarg(call, name):
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def kwarg_str(call, name):
    v = kwarg(call, name)
    return const_str(v) if v is not None else None


def str_list(node):
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return [s for s in (const_str(e) for e in node.elts) if s]
    s = const_str(node)
    return [s] if s else []


# --------------------------------------------------------------------------
# Estruturas
# --------------------------------------------------------------------------

class Effect:
    __slots__ = ("system", "kind", "operation", "file", "line", "order")

    def __init__(self, system, kind, operation, file, line):
        self.system, self.kind, self.operation = system, kind, operation
        self.file, self.line = file, line

    def as_dict(self, rel):
        return {"system": self.system, "kind": self.kind,
                "operation": self.operation, "source": f"{rel}:{self.line}"}


class FuncInfo:
    __slots__ = ("qual", "module", "cls", "name", "file", "line", "items",
                 "decorators", "is_async")

    def __init__(self, qual, module, cls, name, file, line, is_async):
        self.qual, self.module, self.cls, self.name = qual, module, cls, name
        self.file, self.line, self.is_async = file, line, is_async
        self.items = []      # lista ordenada de ("effect", Effect) | ("call", nome, linha)
        self.decorators = []


class ModuleInfo:
    def __init__(self, path, dotted_name):
        self.path = path
        self.dotted = dotted_name
        self.imports = {}          # alias -> modulo raiz
        self.import_from = {}      # alias -> (modulo, nome_original)
        self.app_vars = {}         # var -> {"kind": fastapi|flask|aiohttp, "prefix": str}
        self.routers_included = [] # (var_local_ou_alias, prefix)
        self.funcs = []
        self.strings = []
        self.var_types = {}     # var -> (system, kind)
        self.label_hints = {}   # var -> base_url etc.


# --------------------------------------------------------------------------
# Visitor por arquivo
# --------------------------------------------------------------------------

class ModuleScanner(ast.NodeVisitor):
    def __init__(self, mod: ModuleInfo, project_root: Path, global_vars=None,
                 consts=None):
        self.mod = mod
        self.root = project_root
        self.consts = consts or {}
        self.var_types = dict(global_vars or {})
        self.var_types.update(mod.var_types)
        self.label_hints = dict(mod.label_hints)
        self.stack = []          # pilha de FuncInfo
        self.class_stack = []
        self.rel = str(Path(mod.path).relative_to(project_root))

    def _sval(self, node):
        """String literal ou, se for uma referencia, a constante do projeto.
        Cobre casos como include_router(r, prefix=settings.API_V1_STR)."""
        if node is None:
            return None
        lit = const_str(node)
        if lit is not None:
            return lit
        name = dotted(node)
        if name:
            return self.consts.get(name.split(".")[-1])
        return None

    def _skwarg(self, call, key):
        return self._sval(kwarg(call, key))

    # ---------- imports ----------
    def visit_Import(self, node):
        for a in node.names:
            self.mod.imports[(a.asname or a.name).split(".")[0]] = a.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for a in node.names:
            alias = a.asname or a.name
            self.mod.import_from[alias] = (module, a.name)
            self.mod.imports.setdefault(alias, module)
        self.generic_visit(node)

    # ---------- classes / funcoes ----------
    def visit_ClassDef(self, node):
        self.class_stack.append(node)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        self._function(node, is_async=False)

    def visit_AsyncFunctionDef(self, node):
        self._function(node, is_async=True)

    def _function(self, node, is_async):
        cls = self.class_stack[-1].name if self.class_stack else None
        qual = f"{self.mod.dotted}:{cls + '.' if cls else ''}{node.name}"
        fi = FuncInfo(qual, self.mod.dotted, cls, node.name,
                      self.rel, node.lineno, is_async)
        fi.decorators = node.decorator_list
        self.mod.funcs.append(fi)
        self.stack.append(fi)
        for stmt in node.body:
            self.visit(stmt)
        self.stack.pop()

    # ---------- atribuicoes (apps, routers, blueprints) ----------
    def visit_Assign(self, node):
        val = node.value
        if isinstance(val, ast.Call) and node.targets:
            tgt = node.targets[0]
            if isinstance(tgt, ast.Name):
                self._maybe_app(tgt.id, val)
        for s in (const_str(node.value),):
            if s:
                self.mod.strings.append(s)
        self.generic_visit(node)

    def _maybe_app(self, var, call):
        fn = dotted(call).split(".")[-1]
        if fn in {"FastAPI", "APIRouter", "Blueprint", "Flask", "Quart",
                  "Starlette", "Application", "Api", "Namespace", "Router"}:
            prefix = self._skwarg(call, "prefix") or self._skwarg(call, "url_prefix") or ""
            if not prefix and fn in {"Blueprint", "Namespace"} and len(call.args) > 1:
                p = const_str(call.args[-1])
                prefix = p if p and p.startswith("/") else ""
            kind = {"Flask": "flask", "Quart": "flask", "Blueprint": "flask",
                    "Application": "aiohttp"}.get(fn, "fastapi")
            self.mod.app_vars[var] = {"kind": kind, "prefix": prefix.rstrip("/"),
                                      "factory": fn}

    # ---------- chamadas ----------
    def visit_Call(self, node):
        name = dotted(node.func)
        tail = name.split(".")[-1] if name else ""

        # include_router / register_blueprint / DRF router.register
        if tail in {"include_router", "register_blueprint", "register",
                    "add_namespace", "include"}:
            self._register_group(node, tail)
        elif tail in {"add_api_route", "add_url_rule", "add_route"}:
            self._explicit_route(node, tail)
        elif tail.startswith("add_") and tail[4:] in ROUTE_DECOS:
            self._aiohttp_route(node, tail[4:])
        elif tail in {"path", "re_path", "url"} and "urls" in self.rel:
            self._django_path(node)

        if self.stack:
            self._record_in_function(node, name, tail)
        self.generic_visit(node)

    # ------------------------------------------------------------------
    def _record_in_function(self, node, name, tail):
        fi = self.stack[-1]
        eff = self._match_boundary(node, name, tail)
        if eff:
            fi.items.append(("effect", eff))
            return
        # chamada interna: guardamos o nome para seguir a cadeia depois
        if tail and tail not in {"len", "str", "int", "print", "isinstance",
                                 "append", "format", "dict", "list", "super"}:
            root = name.split(".")[0] if "." in name else ""
            fi.items.append(("call", tail, node.lineno, root))

    def _match_boundary(self, node, name, tail):
        if not name:
            return None
        parts = name.split(".")
        root = parts[0]
        root_mod = self.mod.imports.get(root, root)
        chain_low = name.lower()

        # 1) variavel ja tipada por um construtor conhecido (mais confiavel)
        typed = self.var_types.get(root)
        if typed and len(parts) > 1:
            system, kind = typed
            attrs = SYSTEM_ATTRS.get(system, set())
            if tail in attrs:
                if system == "__SQL__":
                    return Effect("__SQL__", "database",
                                  self._sql_op(node, name, tail), self.rel, node.lineno)
                if system == "__HTTP__":
                    target, op = self._http_op(node, name, tail,
                                               hint=self.label_hints.get(root))
                    return Effect(target, "external_api", op, self.rel, node.lineno)
                return Effect(system, kind,
                              self._generic_op(system, node, name, tail),
                              self.rel, node.lineno)

        for rule in RULES:
            if tail not in rule["attrs"]:
                continue
            root_match = any(root_mod == r or root_mod.startswith(r + ".") or root == r
                             for r in rule["roots"])
            # o modulo aparece em qualquer ponto da cadeia? (ex: redis.asyncio.Redis)
            if not root_match:
                root_match = any(re.search(rf"(^|\.){re.escape(r)}(\.|$)", chain_low)
                                 for r in rule["roots"])
            var_match = bool(re.search(rule["var_re"], chain_low))
            # Django ORM: Model.objects.filter(...)
            django_orm = ".objects." in name + "."
            if not (root_match or var_match or (rule["system"] == "__SQL__" and django_orm)):
                continue
            # Um match apenas por nome de variavel para HTTP e fraco demais se o
            # projeto nem importa lib http; exige um dos dois sinais.
            system = rule["system"]
            if system == "__SQL__":
                return Effect("__SQL__", "database",
                              self._sql_op(node, name, tail), self.rel, node.lineno)
            if system == "__HTTP__":
                target, op = self._http_op(node, name, tail)
                return Effect(target, "external_api", op, self.rel, node.lineno)
            return Effect(system, rule["kind"],
                          self._generic_op(system, node, name, tail),
                          self.rel, node.lineno)
        return None

    # ---------- rotulos de operacao ----------
    def _sql_op(self, node, name, tail):
        for arg in list(node.args) + [k.value for k in node.keywords]:
            s = const_str(arg)
            if s and re.match(r"^\s*(select|insert|update|delete|with|call|merge)\b",
                              s, re.I):
                m = re.match(r"^\s*(\w+)", s.strip())
                verb = m.group(1).upper()
                tbl = re.search(r"\b(?:from|into|update|join)\s+([\w.\"]+)", s, re.I)
                return f"{verb} {tbl.group(1)}" if tbl else verb
        verb = SQL_VERB_BY_METHOD.get(tail, tail.upper())
        entity = self._entity(node, name)
        return f"{verb} {entity}" if entity else verb

    def _entity(self, node, name):
        """Tenta achar a entidade/tabela: Payment.objects.filter, session.query(Payment)."""
        m = re.match(r"^([A-Z]\w+)\.objects\b", name)
        if m:
            return m.group(1).lower()
        for arg in node.args:
            d = dotted(arg)
            if d and re.match(r"^[A-Z]\w+$", d.split(".")[-1]):
                return d.split(".")[-1].lower()
        m = re.search(r"\b(query|select|table|get_or_create)\(", name)
        return None

    def _http_op(self, node, name, tail, hint=None):
        verb = tail.upper() if tail in {"get", "post", "put", "patch", "delete",
                                        "head", "options"} else "CALL"
        url = None
        for arg in node.args[:2]:
            s = const_str(arg)
            if s and ("/" in s or s.startswith("http")):
                url = s
                break
        if url is None:
            u = kwarg_str(node, "url") or kwarg_str(node, "endpoint")
            url = u
        target = (self._target_from_url(url) or self._target_from_url(hint)
                  or self._target_from_var(name))
        path = ""
        if url:
            m = re.match(r"^https?://[^/]+(/.*)?$", url)
            path = (m.group(1) or "/") if m else url
            path = path.split("?")[0]
        return target, (f"{verb} {path}" if path else verb)

    def _target_from_url(self, url):
        if not url:
            return None
        m = re.match(r"^https?://([^/:]+)", url)
        if not m:
            return None
        host = m.group(1)
        if "{" in host:
            return None
        parts = [p for p in host.split(".") if p not in
                 {"www", "com", "br", "net", "io", "org", "local", "svc",
                  "cluster", "internal", "api"}]
        label = parts[0] if parts else host
        return self._camel(label) + "API"

    def _target_from_var(self, name):
        parts = [p for p in name.split(".")[:-1] if p not in {"self", "cls"}]
        cand = parts[-1] if parts else "External"
        cand = re.sub(r"(_?)(client|session|http|adapter|gateway|api|service|"
                      r"connector|integration|proxy|caller|repository)$", "",
                      cand, flags=re.I) or cand
        cand = re.sub(r"^(get_|make_|build_|_)", "", cand)
        if not cand or cand.lower() in {"self", "cls", ""}:
            cand = "External"
        return self._camel(cand) + "API"

    @staticmethod
    def _camel(s):
        s = re.sub(r"[^0-9a-zA-Z_]", "_", s)
        return "".join(p.capitalize() if p.islower() else p
                       for p in s.split("_") if p) or "External"

    def _generic_op(self, system, node, name, tail):
        if system in {"RabbitMQ", "Kafka", "SQS", "Celery"}:
            target = None
            for key in ("routing_key", "queue", "topic", "exchange", "queue_name",
                        "QueueUrl", "name"):
                target = target or kwarg_str(node, key)
            if not target:
                for arg in node.args[:3]:
                    s = const_str(arg)
                    if s and " " not in s and len(s) < 60:
                        target = s
                        break
            verb = "Consume" if "consum" in tail or "receive" in tail else "Publish"
            return f"{verb} {target}" if target else verb
        if system in {"Redis", "Memcached"}:
            key = None
            for arg in node.args[:1]:
                key = const_str(arg)
            if key:
                key = re.sub(r"[:{].*$", "", key).strip(" _-:") or key
                return f"{tail.upper()} {key}"
            return tail.upper()
        if system in {"MongoDB", "Elasticsearch", "DynamoDB"}:
            ent = self._entity(node, name)
            base = re.sub(r"_", " ", tail).upper()
            return f"{base} {ent}" if ent else base
        if system == "S3":
            bucket = kwarg_str(node, "Bucket") or kwarg_str(node, "bucket_name")
            base = re.sub(r"_", " ", tail).title()
            return f"{base} {bucket}" if bucket else base
        if system == "SMTP":
            return "Send email"
        return tail

    # ---------- registro de rotas ----------
    def _register_group(self, node, tail):
        if not node.args:
            return
        target = dotted(node.args[0])
        prefix = (self._skwarg(node, "prefix") or self._skwarg(node, "url_prefix") or "")
        if tail == "register" and len(node.args) >= 2:  # DRF router.register(r'x', ViewSet)
            p = const_str(node.args[0])
            vs = dotted(node.args[1])
            if p is not None and vs:
                self.mod.routers_included.append(("__drf__", "/" + p.strip("/"), vs, None))
                return
        if target:
            parent = None
            full = dotted(node.func).split(".")
            if len(full) >= 2:
                parent = full[-2]
            self.mod.routers_included.append(
                (target, prefix.rstrip("/"), None, parent))

    def _explicit_route(self, node, tail):
        path = const_str(node.args[0]) if node.args else None
        handler = None
        if len(node.args) > 1:
            handler = dotted(node.args[1])
        handler = handler or dotted(kwarg(node, "endpoint") or ast.Constant(""))
        methods = str_list(kwarg(node, "methods")) or ["GET"]
        if path:
            self.mod.routers_included.append(("__explicit__", path,
                                              (handler, methods, node.lineno), None))

    def _aiohttp_route(self, node, verb):
        if not node.args:
            return
        path = const_str(node.args[0])
        handler = dotted(node.args[1]) if len(node.args) > 1 else None
        if path:
            self.mod.routers_included.append(
                ("__explicit__", path, (handler, [verb.upper()], node.lineno), None))

    def _django_path(self, node):
        if not node.args:
            return
        path = const_str(node.args[0])
        if path is None:
            return
        handler = dotted(node.args[1]) if len(node.args) > 1 else None
        if handler and handler.endswith(".as_view"):
            handler = handler[: -len(".as_view")]
        self.mod.routers_included.append(
            ("__explicit__", "/" + path.lstrip("/"), (handler, ["ANY"], node.lineno), None))


# --------------------------------------------------------------------------
# Analisador do projeto
# --------------------------------------------------------------------------

class ProjectAnalyzer:
    def __init__(self, root: Path, args):
        self.root = root
        self.args = args
        self.modules = {}
        self.by_name = {}     # nome simples -> [FuncInfo]
        self.by_qual = {}
        self.warnings = []
        self.consts = {}
        self.flavor_votes = {}
        self.sql_flavor = None
        self.app_title = None

    # ---------- coleta ----------
    def scan(self):
        parsed = []
        for path in self._python_files():
            try:
                src = path.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(src, filename=str(path))
            except (SyntaxError, ValueError) as e:
                self.warnings.append(f"nao consegui parsear {path}: {e}")
                continue
            mod = ModuleInfo(path, self._dotted_name(path))
            self._collect_imports(tree, mod)
            self._collect_consts(tree)
            mod.strings.extend(re.findall(r"[a-z0-9_.]+(?:\+\w+)?://[^\s\"']+", src)[:50])
            mod.strings.extend(re.findall(r"django\.db\.backends\.\w+", src)[:5])
            for rx, flavor in SRC_HINTS:
                n = len(rx.findall(src))
                if n:
                    self.flavor_votes[flavor] = self.flavor_votes.get(flavor, 0) + n
            if self.app_title is None:
                m = re.search(r"FastAPI\([^)]*title\s*=\s*[\"']([^\"']+)", src, re.S)
                if m:
                    self.app_title = m.group(1)
            parsed.append((mod, tree))

        # Fase 1: tipar variaveis (clients, sessions, channels). Duas passadas
        # porque um modulo pode usar um client definido em outro.
        gvars, glabels = {}, {}
        for _ in range(2):
            for mod, tree in parsed:
                vt, lb = dict(gvars), dict(glabels)
                vt.update(mod.var_types)
                lb.update(mod.label_hints)
                VarTypeCollector(mod.imports, vt, lb).visit(tree)
                mod.var_types, mod.label_hints = vt, lb
                gvars.update(vt)
                glabels.update(lb)

        # Fase 2: varredura de rotas e fronteiras
        for mod, tree in parsed:
            scanner = ModuleScanner(mod, self.root, gvars, self.consts)
            scanner.label_hints.update(glabels)
            scanner.visit(tree)
            self.modules[mod.dotted] = mod
            for f in mod.funcs:
                self.by_qual[f.qual] = f
                self.by_name.setdefault(f.name, []).append(f)
        self._detect_sql_flavor()

    def _collect_consts(self, tree):
        for node in ast.walk(tree):
            target, value = None, None
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target, value = node.targets[0], node.value
            elif isinstance(node, ast.AnnAssign):
                target, value = node.target, node.value
            if isinstance(target, ast.Name) and value is not None:
                v = const_str(value)
                if v is not None and len(v) < 200:
                    self.consts.setdefault(target.id, v)

    @staticmethod
    def _collect_imports(tree, mod):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    mod.imports[(a.asname or a.name).split(".")[0]] = a.name
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for a in node.names:
                    alias = a.asname or a.name
                    mod.import_from[alias] = (module, a.name)
                    mod.imports.setdefault(alias, module)

    def _python_files(self):
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames
                           if d not in DEFAULT_EXCLUDES and not d.startswith(".")]
            for fn in sorted(filenames):
                if not fn.endswith(".py"):
                    continue
                p = Path(dirpath) / fn
                rel = str(p.relative_to(self.root))
                if not self.args.include_tests and TEST_HINTS.search(rel.replace(os.sep, "/")):
                    continue
                yield p

    def _dotted_name(self, path: Path):
        rel = path.relative_to(self.root).with_suffix("")
        parts = list(rel.parts)
        if parts and parts[-1] == "__init__":
            parts.pop()
        return ".".join(parts) or "__main__"

    def _detect_sql_flavor(self):
        blob_imports = set()
        for mod in self.modules.values():
            blob_imports.update(mod.imports.values())
            for s in mod.strings:
                for rx, flavor in URL_FLAVOR:
                    if rx.search(s):
                        self.sql_flavor = self.sql_flavor or flavor
        for imp in blob_imports:
            for rx, flavor in SQL_FLAVOR:
                if rx.match(imp):
                    self.sql_flavor = self.sql_flavor or flavor
        if not self.sql_flavor and self.flavor_votes:
            self.sql_flavor = max(self.flavor_votes.items(), key=lambda kv: kv[1])[0]
        if not self.sql_flavor:
            self.sql_flavor = "Database"

    # ---------- endpoints ----------
    def endpoints(self):
        eps = []
        prefixes = self._router_prefixes()
        for mod in self.modules.values():
            for fi in mod.funcs:
                for deco in fi.decorators:
                    found = self._endpoint_from_deco(mod, fi, deco, prefixes)
                    if found:
                        eps.extend(found)
        eps.extend(self._explicit_endpoints(prefixes))
        eps.extend(self._class_based_endpoints(prefixes))
        # dedupe
        seen, out = set(), []
        for ep in sorted(eps, key=lambda e: (e["path"], e["method"])):
            key = (ep["method"], ep["path"], ep["handler"])
            if key in seen:
                continue
            seen.add(key)
            out.append(ep)
        return out

    def _router_prefixes(self):
        """Monta o prefixo completo de cada router, compondo inclusoes aninhadas
        (router de rota -> router de api -> app)."""
        edges, ambiguous, by_name = {}, set(), {}
        for mod in self.modules.values():
            for entry in mod.routers_included:
                target, prefix, extra, parent = entry
                if target.startswith("__"):
                    continue
                child = self._qualify_router(mod, target)
                par = self._qualify_router(mod, parent) if parent else None
                if child in edges and edges[child] != (par, prefix):
                    continue
                edges[child] = (par, prefix)

        def full(key, depth=0):
            if depth > 10 or key not in edges:
                return ""
            parent, prefix = edges[key]
            return (full(parent, depth + 1) if parent else "") + (prefix or "")

        pref = {k: full(k) for k in edges}
        for key, value in list(pref.items()):
            var = key.split(":")[-1]
            if var in by_name and by_name[var] != value:
                ambiguous.add(var)
            by_name[var] = value
        for var, value in by_name.items():
            if var not in ambiguous:
                pref.setdefault(var, value)
        return pref

    def _qualify_router(self, mod, target):
        """'payments.router' no modulo X -> 'app.routers.payments:router'."""
        parts = target.split(".")
        var = parts[-1]
        if len(parts) == 1:
            origin = mod.import_from.get(var)
            owner = origin[0] if origin else mod.dotted
            var = origin[1] if origin else var
        else:
            container = parts[0]
            origin = mod.import_from.get(container)
            if origin:
                owner = f"{origin[0]}.{origin[1]}" if origin[0] else origin[1]
            else:
                owner = mod.imports.get(container, container)
            if len(parts) > 2:
                owner = owner + "." + ".".join(parts[1:-1])
        return f"{self._closest_module(owner)}:{var}"

    def _closest_module(self, dotted_name):
        """Casa um caminho pontuado com um modulo realmente escaneado."""
        if dotted_name in self.modules:
            return dotted_name
        for name in self.modules:
            if name == dotted_name or name.endswith("." + dotted_name):
                return name
        return dotted_name

    def _endpoint_from_deco(self, mod, fi, deco, prefixes):
        call = deco if isinstance(deco, ast.Call) else None
        name = dotted(deco)
        parts = name.split(".")
        if len(parts) < 2:
            return None
        verb = parts[-1]
        var = parts[-2]
        if verb not in ROUTE_DECOS:
            return None
        app = mod.app_vars.get(var)
        if app is None and var not in {"app", "router", "api", "bp", "blueprint"}:
            return None
        path = None
        if call and call.args:
            path = const_str(call.args[0])
        if path is None and call:
            path = kwarg_str(call, "path") or kwarg_str(call, "rule")
        if path is None:
            return None
        methods = ["GET"]
        if verb in {"get", "post", "put", "patch", "delete", "head", "options"}:
            methods = [verb.upper()]
        elif verb in {"route", "api_route"} and call:
            methods = [m.upper() for m in str_list(kwarg(call, "methods"))] or ["GET"]
        elif verb == "websocket":
            methods = ["WS"]
        local_prefix = (app or {}).get("prefix", "")
        outer = prefixes.get(f"{mod.dotted}:{var}") or prefixes.get(var, "")
        full = self._join(outer, local_prefix, path)
        tag = None
        if call:
            tags = str_list(kwarg(call, "tags"))
            tag = tags[0] if tags else None
        return [self._build(fi, m, full, tag) for m in methods]

    def _explicit_endpoints(self, prefixes):
        out = []
        for mod in self.modules.values():
            for target, path, extra, _parent in mod.routers_included:
                if target == "__explicit__" and extra:
                    handler, methods, line = extra
                    fi = self._resolve(handler, mod) if handler else None
                    for m in (methods or ["GET"]):
                        out.append(self._build(fi, m.upper(), path, None,
                                               fallback_handler=handler,
                                               fallback_loc=f"{mod.path.name}:{line}"))
                elif target == "__drf__":
                    vs = extra
                    for m, suffix in (("GET", ""), ("POST", ""), ("GET", "/{id}"),
                                      ("PUT", "/{id}"), ("DELETE", "/{id}")):
                        fi = self._resolve_viewset_method(vs, m, bool(suffix), mod)
                        if fi:
                            out.append(self._build(fi, m, path + suffix, None))
        return out

    def _class_based_endpoints(self, prefixes):
        """APIView/MethodView/ViewSet ja cobertos por urls; aqui so avisamos."""
        return []

    def _resolve_viewset_method(self, vs, method, detail, mod):
        cls = vs.split(".")[-1]
        mapping = {("GET", False): ["list", "get"], ("POST", False): ["create", "post"],
                   ("GET", True): ["retrieve", "get"], ("PUT", True): ["update", "put"],
                   ("DELETE", True): ["destroy", "delete"]}
        for cand in mapping.get((method, detail), []):
            for fi in self.by_name.get(cand, []):
                if fi.cls == cls:
                    return fi
        return None

    def _resolve(self, handler, mod):
        if not handler:
            return None
        simple = handler.split(".")[-1]
        cands = self.by_name.get(simple, [])
        if len(cands) == 1:
            return cands[0]
        for fi in cands:
            if fi.module == mod.dotted:
                return fi
        for fi in cands:
            if handler.split(".")[0] in fi.module:
                return fi
        return cands[0] if cands else None

    @staticmethod
    def _join(*parts):
        segs = [p.strip("/") for p in parts if p]
        return "/" + "/".join(s for s in segs if s)

    def _build(self, fi, method, path, tag, fallback_handler=None,
               fallback_loc=None):
        steps, notes = ([], [])
        if fi:
            steps, notes = self.trace(fi)
        else:
            notes.append(f"handler nao encontrado no projeto: {fallback_handler}")
        return {
            "method": method,
            "path": path,
            "handler": fi.qual if fi else (fallback_handler or "?"),
            "file": fi.file if fi else (fallback_loc or "?"),
            "line": fi.line if fi else 0,
            "tag": tag,
            "async": bool(fi and fi.is_async),
            "steps": steps,
            "notes": notes,
        }

    # ---------- cadeia de chamadas ----------
    def trace(self, fi):
        steps, notes, visited = [], [], set()

        def walk(f, depth):
            if depth > MAX_DEPTH or f.qual in visited:
                return
            visited.add(f.qual)
            for item in f.items:
                if item[0] == "effect":
                    eff = item[1]
                    steps.append(eff.as_dict(eff.file))
                else:
                    _, cname, line, root = item
                    nxt = self._pick(cname, f, root)
                    if nxt:
                        walk(nxt, depth + 1)

        walk(fi, 0)
        noise = {"COMMIT", "FLUSH", "ROLLBACK", "EXECUTE"}
        resolved = []
        for s in steps:
            if s["system"] == "__SQL__":
                s["system"] = self.sql_flavor
            verb = s["operation"].split()[0] if s["operation"] else ""
            if not self.args.keep_tx and verb in noise and s["operation"] == verb:
                continue
            if resolved:
                prev = resolved[-1]
                same_sys = prev["system"] == s["system"]
                prev_verb = prev["operation"].split()[0] if prev["operation"] else ""
                if same_sys and prev["operation"] == s["operation"]:
                    continue
                # `session.execute(...).fetchone()` gera SELECT + SELECT tabela:
                # mantem sempre o rotulo mais especifico.
                if same_sys and prev_verb == verb:
                    if len(s["operation"]) > len(prev["operation"]):
                        resolved[-1] = s
                    continue
            resolved.append(s)
        if not resolved:
            notes.append("nenhuma fronteira detectada - endpoint possivelmente "
                         "puramente computacional ou usa abstracao dinamica")
        return resolved, notes

    def _pick(self, cname, caller, root):
        cands = self.by_name.get(cname)
        if not cands:
            return None
        if root in {"self", "cls"} and caller.cls:
            same = [c for c in cands if c.cls == caller.cls]
            if same:
                return same[0]
        same_mod = [c for c in cands if c.module == caller.module]
        if len(same_mod) == 1:
            return same_mod[0]
        if len(cands) == 1:
            return cands[0]
        if len(cands) <= 3:
            return cands[0]
        return None

    # ---------- consumidores (opcional) ----------
    def consumers(self):
        out = []
        for mod in self.modules.values():
            for fi in mod.funcs:
                names = [dotted(d) for d in fi.decorators]
                if any(re.search(r"(task|subscriber|consumer|agent|listener)",
                                 n, re.I) for n in names):
                    steps, notes = self.trace(fi)
                    out.append({"method": "MSG", "path": f"{fi.name}",
                                "handler": fi.qual, "file": fi.file,
                                "line": fi.line, "tag": "consumer", "async": fi.is_async,
                                "steps": steps, "notes": notes})
        return out


# --------------------------------------------------------------------------
# Montagem do inventario
# --------------------------------------------------------------------------

SYSTEM_SHAPE = {"database": "database", "cache": "database", "queue": "queue",
                "external_api": "service", "storage": "storage"}


def build_inventory(root: Path, args):
    an = ProjectAnalyzer(root, args)
    an.scan()
    eps = an.endpoints()
    if args.include_consumers:
        eps.extend(an.consumers())
    if args.path_filter:
        rx = re.compile(args.path_filter)
        eps = [e for e in eps if rx.search(e["path"])]

    systems = {}
    for ep in eps:
        for st in ep["steps"]:
            key = st["system"]
            systems.setdefault(key, {"label": prettify(key), "kind": st["kind"],
                                     "used_by": 0})
            systems[key]["used_by"] += 1

    app_name = args.app_name or an.app_title or prettify(root.resolve().name)
    return {
        "app_name": app_name,
        "project_root": str(root.resolve()),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "systems": systems,
        "endpoints": eps,
        "stats": {"endpoints": len(eps), "systems": len(systems),
                  "modules": len(an.modules)},
        "warnings": an.warnings + [
            n for ep in eps for n in ep["notes"] if "handler nao encontrado" in n],
    }


def prettify(key):
    known = {"PostgreSQL", "MySQL", "SQLite", "Redis", "RabbitMQ", "Kafka",
             "MongoDB", "Elasticsearch", "DynamoDB", "S3", "SMTP", "SQS",
             "Celery", "Memcached", "SQL Server", "Oracle", "Database"}
    if key in known:
        return key
    s = re.sub(r"API$", " API", key)
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s)
    return s.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", help="raiz do projeto Python")
    ap.add_argument("--out", help="arquivo JSON de saida (default: stdout)")
    ap.add_argument("--app-name", help="nome da API no diagrama")
    ap.add_argument("--include-tests", action="store_true")
    ap.add_argument("--include-consumers", action="store_true",
                    help="tambem mapeia consumidores de fila/tasks como entradas")
    ap.add_argument("--path-filter", help="regex para filtrar endpoints pelo path")
    ap.add_argument("--keep-tx", action="store_true",
                    help="mantem passos de COMMIT/ROLLBACK no fluxo")
    args = ap.parse_args()

    root = Path(args.project).resolve()
    if not root.is_dir():
        sys.exit(f"Diretorio invalido: {root}")

    inv = build_inventory(root, args)
    text = json.dumps(inv, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        s = inv["stats"]
        print(f"OK: {s['endpoints']} endpoints, {s['systems']} fronteiras, "
              f"{s['modules']} modulos -> {args.out}")
        for w in inv["warnings"][:10]:
            print(f"  aviso: {w}")
    else:
        print(text)


if __name__ == "__main__":
    main()
