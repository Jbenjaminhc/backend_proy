import random
from api.models import User

def generate_random_name():
    first_names = ['Pedro', 'Juan', 'Carlos', 'Ana', 'Maria', 'Sofia', 'Luis', 'Gabriel', 'Lucia', 'Marta']
    last_names = ['Renteria', 'Lopez Perez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Sanchez', 'Garcia', 'Diaz', 'Fernandez', 'Perez']

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

def seed_users():
    roles = {
        User.ADMIN: 'admin@admin.com',
        User.CLIENTE_PREMIUM: 'premium@premium.com',
        User.CLIENTE: 'cliente@cliente.com'
    }

    for role, email in roles.items():
        if not User.objects.filter(email=email).exists():
            first_name, last_name = generate_random_name()
            User.objects.create_user(
                email=email,
                password='password',
                first_name=first_name,
                last_name=last_name,
                role=role,
                created_by=email,
                modified_by=email,
            )

