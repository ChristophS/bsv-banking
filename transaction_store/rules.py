from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from banking_readonly.security import ensure_private_directory, protect_file

from .classification import can_be_auto_classified


RULE_SCHEMA_VERSION = 3
CONFLICT_DESCRIPTION_PREFIX = "Mehrere zutreffende Regeln: "


@dataclass(frozen=True)
class RuleCondition:
    connector: str
    match_field: str
    match_operator: str
    match_value: str


@dataclass(frozen=True)
class ClassificationRule:
    rule_id: str
    name: str
    enabled: bool
    match_field: str
    match_operator: str
    match_value: str
    transaction_type: str
    top_category: str
    sub_category: str
    sphere: str
    professional_description: str
    conditions: tuple[RuleCondition, ...] = ()


@dataclass(frozen=True)
class CompletionRule:
    rule_id: str
    name: str
    enabled: bool
    match_field: str
    match_operator: str
    match_value: str
    conditions: tuple[RuleCondition, ...] = ()


TRAINER_BSV_1_RULE = ClassificationRule(
    rule_id="regel_001_verguetung_trainer_bsv_1",
    name="Regel1",
    enabled=True,
    match_field="purpose",
    match_operator="contains",
    match_value="Vergütung Trainer BSV 1",
    transaction_type="Vergütung",
    top_category="Personal und Vergütungen",
    sub_category="Vergütungen - BSV 1",
    sphere="Ideeller Bereich",
    professional_description="Vergütung Trainer BSV 1",
)

CO_TRAINER_BSV_1_RULE = ClassificationRule(
    rule_id="regel_002_verguetung_co_trainer_bsv_1",
    name="Regel2",
    enabled=True,
    match_field="purpose",
    match_operator="contains",
    match_value="Vergütung Co Trainer BSV 1",
    transaction_type="Vergütung",
    top_category="Personal und Vergütungen",
    sub_category="Vergütungen - BSV 1",
    sphere="Ideeller Bereich",
    professional_description="Vergütung Co-Trainer BSV 1",
)

DEFAULT_RULES = (
    TRAINER_BSV_1_RULE,
    CO_TRAINER_BSV_1_RULE,
)

DEFAULT_COMPLETION_RULE = CompletionRule(
    rule_id="abschlussregel_001_verguetung",
    name="Vergütungen automatisch abschließen",
    enabled=True,
    match_field="transaction_type",
    match_operator="equals",
    match_value="Vergütung",
)

_CLASSIFICATION_MATCH_FIELDS = {
    "purpose",
    "counterparty",
    "account_name",
    "account_number",
    "booking_text",
    "amount",
}
_COMPLETION_MATCH_FIELDS = _CLASSIFICATION_MATCH_FIELDS | {
    "transaction_type",
    "top_category",
    "sub_category",
    "sphere",
    "professional_description",
}
_MATCH_OPERATORS = {"contains", "equals", "starts_with", "ends_with"}
_LOGIC_CONNECTORS = {"and", "or", "and_not", "or_not"}
MAX_RULE_CONDITIONS = 50


def connect_rules_database(path: Path) -> sqlite3.Connection:
    ensure_private_directory(path.parent)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    _initialize_rules_schema(connection)
    protect_file(path)
    return connection


def load_classification_rules(
    connection: sqlite3.Connection,
) -> tuple[ClassificationRule, ...]:
    return list_classification_rules(connection, enabled_only=True)


def list_classification_rules(
    connection: sqlite3.Connection,
    enabled_only: bool = False,
) -> tuple[ClassificationRule, ...]:
    where = "WHERE enabled = 1" if enabled_only else ""
    rows = connection.execute(
        f"""
        SELECT
            rule_id, name, enabled, match_field, match_operator, match_value,
            transaction_type, top_category, sub_category, sphere,
            professional_description, conditions_json
        FROM classification_rules
        {where}
        ORDER BY name COLLATE NOCASE, rule_id
        """
    )
    return tuple(_rule_from_row(row) for row in rows)


def load_completion_rules(
    connection: sqlite3.Connection,
) -> tuple[CompletionRule, ...]:
    return list_completion_rules(connection, enabled_only=True)


def list_completion_rules(
    connection: sqlite3.Connection,
    enabled_only: bool = False,
) -> tuple[CompletionRule, ...]:
    where = "WHERE enabled = 1" if enabled_only else ""
    rows = connection.execute(
        f"""
        SELECT
            rule_id, name, enabled, match_field, match_operator,
            match_value, conditions_json
        FROM completion_rules
        {where}
        ORDER BY name COLLATE NOCASE, rule_id
        """
    )
    return tuple(_completion_rule_from_row(row) for row in rows)


def upsert_classification_rule(
    connection: sqlite3.Connection,
    rule: ClassificationRule,
) -> None:
    _validate_rule(rule)
    connection.execute(
        """
        INSERT INTO classification_rules (
            rule_id, name, enabled, match_field, match_operator, match_value,
            transaction_type, top_category, sub_category, sphere,
            professional_description, conditions_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(rule_id) DO UPDATE SET
            name = excluded.name,
            enabled = excluded.enabled,
            match_field = excluded.match_field,
            match_operator = excluded.match_operator,
            match_value = excluded.match_value,
            transaction_type = excluded.transaction_type,
            top_category = excluded.top_category,
            sub_category = excluded.sub_category,
            sphere = excluded.sphere,
            professional_description = excluded.professional_description,
            conditions_json = excluded.conditions_json
        """,
        (
            rule.rule_id,
            rule.name,
            int(rule.enabled),
            rule.match_field,
            rule.match_operator,
            rule.match_value,
            rule.transaction_type,
            rule.top_category,
            rule.sub_category,
            rule.sphere,
            rule.professional_description,
            _conditions_json(_effective_conditions(rule)),
        ),
    )


def upsert_completion_rule(
    connection: sqlite3.Connection,
    rule: CompletionRule,
) -> None:
    _validate_completion_rule(rule)
    connection.execute(
        """
        INSERT INTO completion_rules (
            rule_id, name, enabled, match_field, match_operator,
            match_value, conditions_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(rule_id) DO UPDATE SET
            name = excluded.name,
            enabled = excluded.enabled,
            match_field = excluded.match_field,
            match_operator = excluded.match_operator,
            match_value = excluded.match_value,
            conditions_json = excluded.conditions_json
        """,
        (
            rule.rule_id,
            rule.name,
            int(rule.enabled),
            rule.match_field,
            rule.match_operator,
            rule.match_value,
            _conditions_json(_effective_conditions(rule)),
        ),
    )


def delete_classification_rule(
    connection: sqlite3.Connection,
    rule_id: str,
) -> bool:
    cursor = connection.execute(
        """
        DELETE FROM classification_rules
        WHERE rule_id = ?
        """,
        (rule_id,),
    )
    return cursor.rowcount == 1


def delete_completion_rule(
    connection: sqlite3.Connection,
    rule_id: str,
) -> bool:
    cursor = connection.execute(
        """
        DELETE FROM completion_rules
        WHERE rule_id = ?
        """,
        (rule_id,),
    )
    return cursor.rowcount == 1


def apply_classification_rules(
    connection: sqlite3.Connection,
    rules: Sequence[ClassificationRule],
    transaction_ids: Sequence[str] | None = None,
) -> int:
    changed = 0
    for transaction in _transactions(connection, transaction_ids):
        if not can_be_auto_classified(transaction):
            continue
        matches = matching_rules(transaction, rules)
        if not matches:
            continue
        if len(matches) == 1:
            changed += _apply_single_rule(connection, transaction, matches[0])
        else:
            changed += _mark_rule_conflict(connection, transaction, matches)
    return changed


def matching_rules(
    transaction: object,
    rules: Sequence[ClassificationRule],
) -> tuple[ClassificationRule, ...]:
    return tuple(
        rule
        for rule in rules
        if rule.enabled and _rule_matches(transaction, rule)
    )


def apply_completion_rules(
    connection: sqlite3.Connection,
    rules: Sequence[CompletionRule],
    transaction_ids: Sequence[str] | None = None,
) -> int:
    changed = 0
    _ensure_standard_vorgaenge_for_completion_rules(
        connection,
        rules,
        transaction_ids,
    )
    for vorgangs_id in _automatic_vorgaenge(connection, transaction_ids):
        transactions = _vorgang_transactions(connection, vorgangs_id)
        completed = bool(transactions) and all(
            _has_complete_classification(transaction)
            and matching_completion_rules(transaction, rules)
            for transaction in transactions
        )
        if completed:
            completed = all(
                _has_complete_classification(split)
                for split in _vorgang_splits(connection, vorgangs_id)
            )
        if completed and _vorgang_requires_document(connection, vorgangs_id):
            completed = _vorgang_has_document(connection, vorgangs_id)
        status = "abgeschlossen" if completed else "in_bearbeitung"
        cursor = connection.execute(
            """
            UPDATE vorgaenge
            SET
                status = ?,
                aktualisiert_am = STRFTIME(
                    '%Y-%m-%dT%H:%M:%fZ',
                    'now'
                )
            WHERE vorgangs_id = ?
              AND status_manuell = 0
              AND status <> ?
            """,
            (status, vorgangs_id, status),
        )
        changed += cursor.rowcount
    return changed


def _ensure_standard_vorgaenge_for_completion_rules(
    connection: sqlite3.Connection,
    rules: Sequence[CompletionRule],
    transaction_ids: Sequence[str] | None,
) -> None:
    if not rules:
        return
    for transaction in _completion_rule_candidate_transactions(
        connection,
        transaction_ids,
    ):
        if (
            not _has_complete_classification(transaction)
            or not matching_completion_rules(transaction, rules)
        ):
            continue
        standard_vorgangs_id = f"vorgang_{transaction['transaction_id']}"
        connection.execute(
            """
            INSERT OR IGNORE INTO vorgaenge (
                vorgangs_id,
                vorgangstyp,
                status,
                erstellt_am,
                aktualisiert_am
            ) VALUES (
                ?,
                ?,
                'in_bearbeitung',
                STRFTIME('%Y-%m-%dT%H:%M:%fZ', 'now'),
                STRFTIME('%Y-%m-%dT%H:%M:%fZ', 'now')
            )
            """,
            (standard_vorgangs_id, transaction["transaction_type"]),
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO transaktion_vorgaenge (
                transaktions_id,
                vorgangs_id
            ) VALUES (?, ?)
            """,
            (transaction["transaction_id"], standard_vorgangs_id),
        )


def _completion_rule_candidate_transactions(
    connection: sqlite3.Connection,
    transaction_ids: Sequence[str] | None,
) -> list[sqlite3.Row]:
    columns = """
        t.transaction_id, t.purpose, t.counterparty,
        t.account_name, t.account_number, t.booking_text,
        t.amount, t.transaction_type, t.top_category,
        t.sub_category, t.sphere, t.professional_description
    """
    condition = """
        NOT EXISTS (
            SELECT 1
            FROM transaktion_vorgaenge AS tv
            WHERE tv.transaktions_id = t.transaction_id
        )
    """
    if transaction_ids is None:
        return list(
            connection.execute(
                f"""
                SELECT {columns}
                FROM transactions AS t
                WHERE {condition}
                ORDER BY t.transaction_id
                """
            )
        )

    rows: list[sqlite3.Row] = []
    for offset in range(0, len(transaction_ids), 900):
        chunk = transaction_ids[offset : offset + 900]
        if not chunk:
            continue
        placeholders = ", ".join("?" for _ in chunk)
        rows.extend(
            connection.execute(
                f"""
                SELECT {columns}
                FROM transactions AS t
                WHERE t.transaction_id IN ({placeholders})
                  AND {condition}
                ORDER BY t.transaction_id
                """,
                tuple(chunk),
            )
        )
    return rows


def apply_rule_pipeline(
    connection: sqlite3.Connection,
    classification_rules: Sequence[ClassificationRule],
    completion_rules: Sequence[CompletionRule],
    transaction_ids: Sequence[str] | None = None,
) -> tuple[int, int]:
    classified = apply_classification_rules(
        connection,
        classification_rules,
        transaction_ids,
    )
    completed = apply_completion_rules(
        connection,
        completion_rules,
        transaction_ids,
    )
    return classified, completed


def matching_completion_rules(
    transaction: object,
    rules: Sequence[CompletionRule],
) -> tuple[CompletionRule, ...]:
    return tuple(
        rule
        for rule in rules
        if rule.enabled and _rule_matches(transaction, rule)
    )


def _apply_single_rule(
    connection: sqlite3.Connection,
    transaction: sqlite3.Row,
    rule: ClassificationRule,
) -> int:
    cursor = connection.execute(
        """
        UPDATE transactions
        SET
            transaction_type = ?,
            top_category = ?,
            sub_category = ?,
            sphere = ?,
            professional_description = ?
        WHERE transaction_id = ?
          AND TRIM(COALESCE(transaction_type, '')) = ''
          AND TRIM(COALESCE(top_category, '')) = ''
          AND TRIM(COALESCE(sub_category, '')) = ''
          AND TRIM(COALESCE(sphere, '')) = ''
          AND TRIM(COALESCE(professional_description, '')) = ''
        """,
        (
            rule.transaction_type,
            rule.top_category,
            rule.sub_category,
            rule.sphere,
            rule.professional_description,
            transaction["transaction_id"],
        ),
    )
    return cursor.rowcount


def _mark_rule_conflict(
    connection: sqlite3.Connection,
    transaction: sqlite3.Row,
    rules: Sequence[ClassificationRule],
) -> int:
    description = CONFLICT_DESCRIPTION_PREFIX + ", ".join(
        rule.name for rule in rules
    )
    cursor = connection.execute(
        """
        UPDATE transactions
        SET professional_description = ?
        WHERE transaction_id = ?
          AND TRIM(COALESCE(transaction_type, '')) = ''
          AND TRIM(COALESCE(top_category, '')) = ''
          AND TRIM(COALESCE(sub_category, '')) = ''
          AND TRIM(COALESCE(sphere, '')) = ''
          AND TRIM(COALESCE(professional_description, '')) = ''
        """,
        (description, transaction["transaction_id"]),
    )
    return cursor.rowcount


def _rule_matches(
    transaction: object,
    rule: ClassificationRule | CompletionRule,
) -> bool:
    conditions = _effective_conditions(rule)
    group_value = _condition_matches(transaction, conditions[0])
    expression_value = False
    for condition in conditions[1:]:
        condition_value = _condition_matches(transaction, condition)
        if condition.connector == "and":
            group_value = group_value and condition_value
        elif condition.connector == "and_not":
            group_value = group_value and not condition_value
        elif condition.connector in {"or", "or_not"}:
            expression_value = expression_value or group_value
            group_value = (
                condition_value
                if condition.connector == "or"
                else not condition_value
            )
        else:
            raise ValueError(
                f"Nicht unterstuetzte Logikverknuepfung: {condition.connector}"
            )
    return expression_value or group_value


def _condition_matches(
    transaction: object,
    condition: RuleCondition,
) -> bool:
    actual = _normalize(_read_value(transaction, condition.match_field))
    expected = _normalize(condition.match_value)
    if condition.match_operator == "contains":
        return expected in actual
    if condition.match_operator == "equals":
        return actual == expected
    if condition.match_operator == "starts_with":
        return actual.startswith(expected)
    if condition.match_operator == "ends_with":
        return actual.endswith(expected)
    raise ValueError(
        f"Nicht unterstuetzter Regeloperator: {condition.match_operator}"
    )


def _transactions(
    connection: sqlite3.Connection,
    transaction_ids: Sequence[str] | None,
) -> list[sqlite3.Row]:
    columns = """
        transaction_id, purpose, counterparty, account_name, account_number,
        booking_text, amount, transaction_type, top_category, sub_category,
        sphere, professional_description
    """
    if transaction_ids is None:
        return list(connection.execute(f"SELECT {columns} FROM transactions"))
    rows = []
    for offset in range(0, len(transaction_ids), 900):
        chunk = transaction_ids[offset : offset + 900]
        if not chunk:
            continue
        placeholders = ", ".join("?" for _ in chunk)
        rows.extend(
            connection.execute(
                f"""
                SELECT {columns}
                FROM transactions
                WHERE transaction_id IN ({placeholders})
                """,
                tuple(chunk),
            )
        )
    return rows


def _automatic_vorgaenge(
    connection: sqlite3.Connection,
    transaction_ids: Sequence[str] | None,
) -> list[str]:
    if transaction_ids is None:
        return [
            str(row[0])
            for row in connection.execute(
                """
                SELECT vorgangs_id
                FROM vorgaenge
                WHERE status_manuell = 0
                ORDER BY vorgangs_id
                """
            )
        ]
    result: set[str] = set()
    for offset in range(0, len(transaction_ids), 900):
        chunk = transaction_ids[offset : offset + 900]
        if not chunk:
            continue
        placeholders = ", ".join("?" for _ in chunk)
        result.update(
            str(row[0])
            for row in connection.execute(
                f"""
                SELECT DISTINCT tv.vorgangs_id
                FROM transaktion_vorgaenge AS tv
                JOIN vorgaenge AS v
                  ON v.vorgangs_id = tv.vorgangs_id
                WHERE tv.transaktions_id IN ({placeholders})
                  AND v.status_manuell = 0
                """,
                tuple(chunk),
            )
        )
    return sorted(result)


def _vorgang_transactions(
    connection: sqlite3.Connection,
    vorgangs_id: str,
) -> list[sqlite3.Row]:
    return list(
        connection.execute(
            """
            SELECT
                t.transaction_id, t.purpose, t.counterparty,
                t.account_name, t.account_number, t.booking_text,
                t.amount, t.transaction_type, t.top_category,
                t.sub_category, t.sphere, t.professional_description
            FROM transaktion_vorgaenge AS tv
            JOIN transactions AS t
              ON t.transaction_id = tv.transaktions_id
            WHERE tv.vorgangs_id = ?
            ORDER BY t.transaction_id
            """,
            (vorgangs_id,),
        )
    )


def _vorgang_splits(
    connection: sqlite3.Connection,
    vorgangs_id: str,
) -> list[sqlite3.Row]:
    """Return splits relevant to a Vorgang through explicit or inherited links."""
    return list(
        connection.execute(
            """
            SELECT
                split.transaction_type, split.top_category,
                split.sub_category, split.sphere,
                split.professional_description
            FROM transaction_splits AS split
            WHERE split.vorgangs_id = ?
               OR (
                    split.vorgangs_id IS NULL
                    AND EXISTS (
                        SELECT 1
                        FROM transaktion_vorgaenge AS tv
                        WHERE tv.transaktions_id = split.transaction_id
                          AND tv.vorgangs_id = ?
                    )
               )
            ORDER BY split.transaction_id, split.sort_order, split.rowid
            """,
            (vorgangs_id, vorgangs_id),
        )
    )


def _has_complete_classification(transaction: object) -> bool:
    return all(
        _read_value(transaction, field).strip()
        for field in (
            "transaction_type",
            "top_category",
            "sub_category",
            "sphere",
        )
    )


def _vorgang_requires_document(
    connection: sqlite3.Connection,
    vorgangs_id: str,
) -> bool:
    row = connection.execute(
        """
        SELECT vorgangstyp
        FROM vorgaenge
        WHERE vorgangs_id = ?
        """,
        (vorgangs_id,),
    ).fetchone()
    return str(row["vorgangstyp"] if row else "").strip().casefold() == "rechnung"


def _vorgang_has_document(
    connection: sqlite3.Connection,
    vorgangs_id: str,
) -> bool:
    return (
        connection.execute(
            """
            SELECT 1
            FROM vorgang_belege
            WHERE vorgangs_id = ?
            LIMIT 1
            """,
            (vorgangs_id,),
        ).fetchone()
        is not None
    )


def _initialize_rules_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS schema_info (
            version INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS classification_rules (
            rule_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            enabled INTEGER NOT NULL CHECK(enabled IN (0, 1)),
            match_field TEXT NOT NULL,
            match_operator TEXT NOT NULL,
            match_value TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            top_category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            sphere TEXT NOT NULL,
            professional_description TEXT NOT NULL,
            conditions_json TEXT NOT NULL DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS completion_rules (
            rule_id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            enabled INTEGER NOT NULL CHECK(enabled IN (0, 1)),
            match_field TEXT NOT NULL,
            match_operator TEXT NOT NULL,
            match_value TEXT NOT NULL,
            conditions_json TEXT NOT NULL DEFAULT '[]'
        );
        """
    )
    row = connection.execute(
        "SELECT version FROM schema_info LIMIT 1"
    ).fetchone()
    seed_default_rules = False
    if row is None:
        connection.execute(
            "INSERT INTO schema_info(version) VALUES (?)",
            (RULE_SCHEMA_VERSION,),
        )
        seed_default_rules = True
    elif row[0] == 1:
        columns = {
            item["name"]
            for item in connection.execute(
                "PRAGMA table_info(classification_rules)"
            )
        }
        if "conditions_json" not in columns:
            connection.execute(
                """
                ALTER TABLE classification_rules
                ADD COLUMN conditions_json TEXT NOT NULL DEFAULT '[]'
                """
            )
        rows = connection.execute(
            """
            SELECT
                rule_id, match_field, match_operator, match_value
            FROM classification_rules
            """
        ).fetchall()
        for existing_rule in rows:
            condition = RuleCondition(
                connector="",
                match_field=existing_rule["match_field"],
                match_operator=existing_rule["match_operator"],
                match_value=existing_rule["match_value"],
            )
            connection.execute(
                """
                UPDATE classification_rules
                SET conditions_json = ?
                WHERE rule_id = ?
                """,
                (
                    _conditions_json((condition,)),
                    existing_rule["rule_id"],
                ),
            )
        connection.execute("UPDATE schema_info SET version = 2")
        seed_default_rules = True
        row = (2,)
    if row is not None and row[0] == 2:
        connection.execute(
            "UPDATE schema_info SET version = ?",
            (RULE_SCHEMA_VERSION,),
        )
        seed_default_rules = True
    elif row is not None and row[0] != RULE_SCHEMA_VERSION:
        raise RuntimeError(
            f"Nicht unterstuetzte Regeldatenbankversion: {row[0]}"
        )
    try:
        if seed_default_rules:
            for rule in DEFAULT_RULES:
                existing = connection.execute(
                    """
                    SELECT 1
                    FROM classification_rules
                    WHERE rule_id = ?
                    """,
                    (rule.rule_id,),
                ).fetchone()
                if existing is None:
                    upsert_classification_rule(connection, rule)
            existing_completion_rule = connection.execute(
                """
                SELECT 1
                FROM completion_rules
                WHERE rule_id = ?
                """,
                (DEFAULT_COMPLETION_RULE.rule_id,),
            ).fetchone()
            if existing_completion_rule is None:
                upsert_completion_rule(
                    connection,
                    DEFAULT_COMPLETION_RULE,
                )
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def _validate_rule(rule: ClassificationRule) -> None:
    if not rule.rule_id.strip() or not rule.name.strip():
        raise ValueError("Regel-ID und Regelname duerfen nicht leer sein.")
    conditions = _effective_conditions(rule)
    _validate_conditions(conditions, _CLASSIFICATION_MATCH_FIELDS)
    required_values = (
        rule.transaction_type,
        rule.top_category,
        rule.sub_category,
        rule.sphere,
    )
    if any(not value.strip() for value in required_values):
        raise ValueError(
            "Eine Klassifikationsregel muss alle Pflichtfelder setzen."
        )


def _validate_completion_rule(rule: CompletionRule) -> None:
    if not rule.rule_id.strip() or not rule.name.strip():
        raise ValueError("Regel-ID und Regelname duerfen nicht leer sein.")
    _validate_conditions(
        _effective_conditions(rule),
        _COMPLETION_MATCH_FIELDS,
    )


def _validate_conditions(
    conditions: Sequence[RuleCondition],
    match_fields: set[str],
) -> None:
    if not conditions:
        raise ValueError("Eine Regel muss mindestens eine Bedingung enthalten.")
    if len(conditions) > MAX_RULE_CONDITIONS:
        raise ValueError(
            f"Eine Regel darf höchstens {MAX_RULE_CONDITIONS} Bedingungen "
            "enthalten."
        )
    for index, condition in enumerate(conditions):
        if index == 0 and condition.connector:
            raise ValueError(
                "Die erste Bedingung darf keine Logikverknüpfung haben."
            )
        if index > 0 and condition.connector not in _LOGIC_CONNECTORS:
            raise ValueError(
                "Jede weitere Bedingung benötigt UND, ODER, "
                "OHNE oder ODER NICHT."
            )
        if condition.match_field not in match_fields:
            raise ValueError(
                f"Nicht unterstuetztes Regelfeld: {condition.match_field}"
            )
        if condition.match_operator not in _MATCH_OPERATORS:
            raise ValueError(
                "Nicht unterstuetzter Regeloperator: "
                f"{condition.match_operator}"
            )
        if not condition.match_value.strip():
            raise ValueError(
                f"Der Vergleichswert der Bedingung {index + 1} "
                "darf nicht leer sein."
            )
    _validate_condition_logic(conditions)


def _rule_from_row(row: sqlite3.Row) -> ClassificationRule:
    conditions = _conditions_from_json(row["conditions_json"])
    if not conditions:
        conditions = (
            RuleCondition(
                connector="",
                match_field=row["match_field"],
                match_operator=row["match_operator"],
                match_value=row["match_value"],
            ),
        )
    return ClassificationRule(
        rule_id=row["rule_id"],
        name=row["name"],
        enabled=bool(row["enabled"]),
        match_field=row["match_field"],
        match_operator=row["match_operator"],
        match_value=row["match_value"],
        transaction_type=row["transaction_type"],
        top_category=row["top_category"],
        sub_category=row["sub_category"],
        sphere=row["sphere"],
        professional_description=row["professional_description"],
        conditions=conditions,
    )


def _completion_rule_from_row(row: sqlite3.Row) -> CompletionRule:
    conditions = _conditions_from_json(row["conditions_json"])
    if not conditions:
        conditions = (
            RuleCondition(
                connector="",
                match_field=row["match_field"],
                match_operator=row["match_operator"],
                match_value=row["match_value"],
            ),
        )
    return CompletionRule(
        rule_id=row["rule_id"],
        name=row["name"],
        enabled=bool(row["enabled"]),
        match_field=row["match_field"],
        match_operator=row["match_operator"],
        match_value=row["match_value"],
        conditions=conditions,
    )


def _effective_conditions(
    rule: ClassificationRule | CompletionRule,
) -> tuple[RuleCondition, ...]:
    if rule.conditions:
        return rule.conditions
    return (
        RuleCondition(
            connector="",
            match_field=rule.match_field,
            match_operator=rule.match_operator,
            match_value=rule.match_value,
        ),
    )


def _conditions_json(conditions: Sequence[RuleCondition]) -> str:
    return json.dumps(
        [
            {
                "connector": condition.connector,
                "match_field": condition.match_field,
                "match_operator": condition.match_operator,
                "match_value": condition.match_value,
            }
            for condition in conditions
        ],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def _conditions_from_json(value: str) -> tuple[RuleCondition, ...]:
    try:
        raw_conditions = json.loads(value or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError("Ungültige gespeicherte Regelbedingungen.") from exc
    if not isinstance(raw_conditions, list):
        raise RuntimeError("Ungültige gespeicherte Regelbedingungen.")
    result = []
    for raw_condition in raw_conditions:
        if not isinstance(raw_condition, dict):
            raise RuntimeError("Ungültige gespeicherte Regelbedingung.")
        result.append(
            RuleCondition(
                connector=str(raw_condition.get("connector", "")),
                match_field=str(raw_condition.get("match_field", "")),
                match_operator=str(raw_condition.get("match_operator", "")),
                match_value=str(raw_condition.get("match_value", "")),
            )
        )
    return tuple(result)


def _condition_key(condition: RuleCondition) -> tuple[str, str, str]:
    return (
        condition.match_field,
        condition.match_operator,
        _normalize(condition.match_value),
    )


def _validate_condition_logic(
    conditions: Sequence[RuleCondition],
) -> None:
    groups: list[list[tuple[tuple[str, str, str], bool]]] = [[]]
    for index, condition in enumerate(conditions):
        negated = condition.connector in {"and_not", "or_not"}
        if index > 0 and condition.connector in {"or", "or_not"}:
            groups.append([])
        key = _condition_key(condition)
        group = groups[-1]
        if any(
            existing_key == key and existing_negated != negated
            for existing_key, existing_negated in group
        ):
            raise ValueError(
                "Die Bedingungen enthalten einen direkten Widerspruch: "
                "dieselbe Bedingung wird zugleich verlangt und ausgeschlossen."
            )
        group.append((key, negated))

    singleton_groups: dict[tuple[str, str, str], bool] = {}
    for group in groups:
        if len(group) != 1:
            continue
        key, negated = group[0]
        if key in singleton_groups and singleton_groups[key] != negated:
            raise ValueError(
                "Die Regel wäre immer wahr, weil eine Bedingung mit ihrem "
                "Gegenteil per ODER verknüpft ist."
            )
        singleton_groups[key] = negated


def _read_value(transaction: object, field: str) -> str:
    try:
        value = transaction[field]  # type: ignore[index]
    except (IndexError, KeyError, TypeError):
        value = getattr(transaction, field, None)
    return "" if value is None else str(value)


def _normalize(value: str) -> str:
    return " ".join(value.split()).casefold()
