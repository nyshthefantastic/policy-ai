from pathlib import Path

from sqlalchemy import text

from app.db.session import engine


def init_db() -> None:
    schema_path = Path(__file__).parent / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    with engine.begin() as conn:
        conn.execute(text(schema_sql))

        conn.execute(
            text(
                """
                INSERT INTO tenants (id, name)
                VALUES (:id, :name)
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {"id": "acme", "name": "Acme Corporation"},
        )


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")