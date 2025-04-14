import random
from api.models import User,Role

def generate_random_name():
    first_names = ['Pedro', 'Juan', 'Carlos', 'Ana', 'Maria', 'Sofia', 'Luis', 'Gabriel', 'Lucia', 'Marta']
    last_names = ['Renteria', 'Lopez Perez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Sanchez', 'Garcia', 'Diaz', 'Fernandez', 'Perez']

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

def seed_users():
    admin_role, _ = Role.objects.get_or_create(name='Admin')
    premium_role, _ = Role.objects.get_or_create(name='Premium')
    cliente_role, _ = Role.objects.get_or_create(name='Cliente')

    
    users_data = [
        {
            'email': 'admin@admin.com',
            'roles': [admin_role, premium_role, cliente_role]
        },
        {
            'email': 'premium@premium.com',
            'roles': [premium_role, cliente_role]
        },
        {
            'email': 'cliente@cliente.com',
            'roles': [cliente_role]
        }
    ]

    for data in users_data:
        email = data['email']
        if not User.objects.filter(email=email).exists():
            first_name, last_name = generate_random_name()
            user = User.objects.create_user(
                email=email,
                password='password',
                first_name=first_name,
                last_name=last_name,
                created_by=email,
                modified_by=email
            )
            user.roles.set(data['roles'])
            user.save()

