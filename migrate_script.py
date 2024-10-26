import os

from flask_migrate import upgrade, migrate, init

from app import create_app, db


def reset_database():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Database dropped.")

        # Recreate all tables
        db.create_all()
        print("Database created.")

        # Initialize migration directory if not already done
        migrations_path = os.path.join(app.root_path, 'migrations')
        if not os.path.exists(migrations_path):
            init()
            print("Initialized migration directory.")

        # Generate and apply migrations
        migrate(message="Recreate database with new fields")
        upgrade()
        print("Database migrated and upgraded.")


if __name__ == '__main__':
    reset_database()
