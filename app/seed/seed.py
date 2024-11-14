from app import db
from app.models.category import Category
from app.models.role import Role
from app.models.user import User


def seed_data(app):
    """Seed the database with initial data."""
    with app.app_context():
        try:
            # Seed roles if they don't exist
            if Role.query.count() == 0:
                admin_role = Role(name='admin')
                user_role = Role(name='normal user')

                db.session.add(admin_role)
                db.session.add(user_role)

                # Seed users
                admin_user = User(
                    name='Admin',
                    gender='Male',
                    phone="012345678",
                    email='admin@gmail.com',
                    address="Phnom Penh",
                    role=admin_role
                )
                admin_user.set_password('admin')

                normal_user = User(
                    name='Normal',
                    gender='Female',
                    phone="012345677",
                    email='user@gmail.com',
                    address="Phnom Penh",
                    role=user_role
                )
                normal_user.set_password('normal')

                db.session.add(admin_user)
                db.session.add(normal_user)

                db.session.commit()
                print("Roles and users seeded successfully.")
            else:
                print("Roles already exist. Skipping role and user seeding.")

            # Seed categories if they don't exist
            if Category.query.count() == 0:
                category1 = Category(
                    category_name='Food',
                    description='All things Food-related',
                    user_id=admin_user.id
                )
                category2 = Category(
                    category_name='Drink',
                    description='Lifestyle and daily living drinking product',
                    user_id=admin_user.id
                )

                db.session.add(category1)
                db.session.add(category2)

                db.session.commit()
                print("Categories seeded successfully.")
            else:
                print("Categories already exist. Skipping category seeding.")

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while seeding the database: {e}")
