# app/seed/seed.py
from app import create_app, db
from app.models.role import Role
from app.models.user import User


def seed_data():
    app = create_app()
    with app.app_context():
        if Role.query.count() == 0:
            admin_role = Role(name='admin')
            user_role = Role(name='normal user')

            db.session.add(admin_role)
            db.session.add(user_role)

            admin_user = User(name='Admin', email='admin@gmail.com', role=admin_role)
            admin_user.set_password('adminpassword')

            normal_user = User(name='Normal', email='user@gmail.com', role=user_role)
            normal_user.set_password('userpassword')

            db.session.add(admin_user)
            db.session.add(normal_user)

            db.session.commit()

            print("Database seeded successfully.")
        else:
            print("Roles already exist. Skipping seeding.")


if __name__ == '__main__':
    seed_data()
