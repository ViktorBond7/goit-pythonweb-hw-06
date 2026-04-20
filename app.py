import argparse
from datetime import datetime
from sqlalchemy.orm import Session
from src.database.connect import engine
from src.database.models import Grade, Group, Student, Subject, Teacher

MODEL_MAP = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}

CREATE_REQUIRED_FIELDS = {
    "Teacher": ["name"],
    "Group": ["name"],
    "Student": ["name", "group_id"],
    "Subject": ["name", "teacher_id"],
    "Grade": ["student_id", "subject_id", "grade"],
}

UPDATE_ALLOWED_FIELDS = {
    "Teacher": ["name"],
    "Group": ["name"],
    "Student": ["name", "group_id"],
    "Subject": ["name", "teacher_id"],
    "Grade": ["student_id", "subject_id", "grade", "created_at"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CLI for CRUD operations")

    parser.add_argument(
        "-a", "--action", required=True, choices=["create", "list", "update", "remove"]
    )
    parser.add_argument("-m", "--model", required=True, choices=list(MODEL_MAP.keys()))

    parser.add_argument("--id", type=int)
    parser.add_argument("--name")
    parser.add_argument("--group_id", type=int)
    parser.add_argument("--teacher_id", type=int)
    parser.add_argument("--student_id", type=int)
    parser.add_argument("--subject_id", type=int)
    parser.add_argument("--grade", type=int)
    parser.add_argument("--created_at", help="ISO format, example: 2026-04-20T15:30:00")

    return parser.parse_args()


def build_payload(args: argparse.Namespace, fields: list[str]) -> dict:
    payload = {}
    for field in fields:
        value = getattr(args, field)
        if value is not None:
            payload[field] = value
    print("Payload:", payload)
    return payload


def normalize_created_at(payload: dict) -> dict:
    if "created_at" in payload and isinstance(payload["created_at"], str):
        payload["created_at"] = datetime.fromisoformat(payload["created_at"])
    print("Normalized Payload:", payload)
    return payload


def create_entity(session: Session, model_name: str, args: argparse.Namespace) -> None:
    model_cls = MODEL_MAP[model_name]
    required_fields = CREATE_REQUIRED_FIELDS[model_name]

    payload = build_payload(args, required_fields + ["created_at"])
    payload = normalize_created_at(payload)

    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        raise ValueError(
            f"Missing required fields for create: {', '.join(missing_fields)}"
        )

    entity = model_cls(**payload)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    print(f"Created: {entity}")


def list_entities(session: Session, model_name: str) -> None:
    model_cls = MODEL_MAP[model_name]
    entities = session.query(model_cls).all()
    if not entities:
        print("No records found")
        return

    for entity in entities:
        print(entity)


def update_entity(session: Session, model_name: str, args: argparse.Namespace) -> None:
    if args.id is None:
        raise ValueError("--id is required for update")

    model_cls = MODEL_MAP[model_name]
    entity = session.get(model_cls, args.id)
    if entity is None:
        print(f"{model_name} with id={args.id} not found")
        return

    payload = build_payload(args, UPDATE_ALLOWED_FIELDS[model_name])
    payload = normalize_created_at(payload)

    if not payload:
        raise ValueError("No fields provided for update")

    for key, value in payload.items():
        setattr(entity, key, value)

    session.commit()
    session.refresh(entity)
    print(f"Updated: {entity}")


def remove_entity(session: Session, model_name: str, args: argparse.Namespace) -> None:
    if args.id is None:
        raise ValueError("--id is required for remove")

    model_cls = MODEL_MAP[model_name]
    entity = session.get(model_cls, args.id)
    if entity is None:
        print(f"{model_name} with id={args.id} not found")
        return

    session.delete(entity)
    session.commit()
    print(f"Removed: {entity}")


def main() -> None:
    args = parse_args()

    with Session(engine) as session:
        if args.action == "create":
            create_entity(session, args.model, args)
        elif args.action == "list":
            list_entities(session, args.model)
        elif args.action == "update":
            update_entity(session, args.model, args)
        elif args.action == "remove":
            remove_entity(session, args.model, args)


if __name__ == "__main__":
    main()

