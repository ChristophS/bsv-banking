from __future__ import annotations

from enum import Enum
from typing import Iterable, Mapping


class ClassificationStatus(str, Enum):
    UNCLASSIFIED = "unklassifiziert"
    FULLY_CLASSIFIED = "vollstaendig_klassifiziert"
    INCOMPLETELY_CLASSIFIED = "unvollstaendig_klassifiziert"


REQUIRED_CLASSIFICATION_FIELDS = (
    "transaction_type",
    "top_category",
    "sub_category",
    "sphere",
)
OPTIONAL_CLASSIFICATION_FIELDS = ("professional_description",)
CLASSIFICATION_FIELDS = (
    *REQUIRED_CLASSIFICATION_FIELDS,
    *OPTIONAL_CLASSIFICATION_FIELDS,
)

_FIELD_ALIASES = {
    "transaction_type": ("transaction_type", "transaktionstyp"),
    "top_category": ("top_category", "oberkategorie"),
    "sub_category": ("sub_category", "unterkategorie"),
    "sphere": ("sphere", "sphaere"),
    "professional_description": (
        "professional_description",
        "fachliche_beschreibung",
    ),
}

SQL_CLASSIFICATION_STATUS_EXPRESSION = """
CASE
    WHEN
        TRIM(COALESCE(transaction_type, '')) = ''
        AND TRIM(COALESCE(top_category, '')) = ''
        AND TRIM(COALESCE(sub_category, '')) = ''
        AND TRIM(COALESCE(sphere, '')) = ''
        AND TRIM(COALESCE(professional_description, '')) = ''
    THEN 'unklassifiziert'
    WHEN
        TRIM(COALESCE(transaction_type, '')) <> ''
        AND TRIM(COALESCE(top_category, '')) <> ''
        AND TRIM(COALESCE(sub_category, '')) <> ''
        AND TRIM(COALESCE(sphere, '')) <> ''
    THEN 'vollstaendig_klassifiziert'
    ELSE 'unvollstaendig_klassifiziert'
END
""".strip()


def classification_status(transaction: object) -> ClassificationStatus:
    values = {
        field: _field_value(transaction, field)
        for field in CLASSIFICATION_FIELDS
    }
    if all(not value for value in values.values()):
        return ClassificationStatus.UNCLASSIFIED
    if all(values[field] for field in REQUIRED_CLASSIFICATION_FIELDS):
        return ClassificationStatus.FULLY_CLASSIFIED
    return ClassificationStatus.INCOMPLETELY_CLASSIFIED


def aggregate_classification_status(
    items: Iterable[object],
) -> ClassificationStatus:
    statuses = [classification_status(item) for item in items]
    if not statuses:
        return ClassificationStatus.UNCLASSIFIED
    if all(status is ClassificationStatus.UNCLASSIFIED for status in statuses):
        return ClassificationStatus.UNCLASSIFIED
    if all(
        status is ClassificationStatus.FULLY_CLASSIFIED
        for status in statuses
    ):
        return ClassificationStatus.FULLY_CLASSIFIED
    return ClassificationStatus.INCOMPLETELY_CLASSIFIED


def can_be_auto_classified(transaction: object) -> bool:
    return classification_status(transaction) is ClassificationStatus.UNCLASSIFIED


def requires_manual_classification_review(transaction: object) -> bool:
    return (
        classification_status(transaction)
        is ClassificationStatus.INCOMPLETELY_CLASSIFIED
    )


def _field_value(transaction: object, field: str) -> str:
    for alias in _FIELD_ALIASES[field]:
        value = _read_value(transaction, alias)
        if value is not None:
            return str(value).strip()
    return ""


def _read_value(transaction: object, field: str) -> object | None:
    if isinstance(transaction, Mapping):
        return transaction.get(field)
    try:
        return transaction[field]  # type: ignore[index]
    except (IndexError, KeyError, TypeError):
        pass
    return getattr(transaction, field, None)
