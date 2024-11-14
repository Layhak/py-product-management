from app import db
from app.models.category import Category
from app.models.product import Product
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
                food_category = Category(
                    category_name='Food',
                    description='All things food-related',
                    user_id=admin_user.id
                )
                drink_category = Category(
                    category_name='Drink',
                    description='All things drink-related',
                    user_id=admin_user.id
                )

                db.session.add(food_category)
                db.session.add(drink_category)

                db.session.commit()
                print("Categories seeded successfully.")
            else:
                print("Categories already exist. Skipping category seeding.")

            # Seed products if they don't exist
            if Product.query.count() == 0:
                coca_cola = Product(
                    product_name='Coca Cola',
                    category_id=drink_category.id,
                    user_id=admin_user.id,
                    price=1.5,
                    qty=100,
                    image='coca.png'
                )
                burger = Product(
                    product_name='Burger',
                    category_id=food_category.id,
                    user_id=admin_user.id,
                    price=5.0,
                    qty=50,
                    image='burger.png'
                )

                db.session.add(coca_cola)
                db.session.add(burger)

                db.session.commit()
                print("Products seeded successfully.")
            else:
                print("Products already exist. Skipping product seeding.")

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while seeding the database: {e}")
