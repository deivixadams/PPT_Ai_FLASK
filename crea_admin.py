import sys
from app import db, user_datastore, app
from app import User, Role

def create_admin():
    # Asegura que la aplicación está en contexto
    with app.app_context():
        # Crear el rol de administrador si no existe
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
            print("Role 'admin' created successfully.")
        else:
            print("Role 'admin' already exists.")

        admin_email = 'admin@gmail.com'  # Reemplaza con el email que prefieras
        admin_password = 'lafesalva'  # Reemplaza con una contraseña segura
        
        # Crea el nuevo usuario administrador
        admin_user = user_datastore.create_user(email=admin_email, password=admin_password)
        user_datastore.add_role_to_user(admin_user, admin_role)
        db.session.commit()
        print(f"Admin user {admin_email} created successfully with new password.")

def delete_admin():
    # Asegura que la aplicación está en contexto
    with app.app_context():
        admin_email = 'admin@example.com'  # Reemplaza con el email que prefieras
        
        # Busca si el usuario administrador ya existe
        admin_user = User.query.filter_by(email=admin_email).first()
        if admin_user:
            # Si el usuario administrador ya existe, elimínalo
            print(f"Admin user {admin_email} already exists. Deleting.")
            db.session.delete(admin_user)
            db.session.commit()
            print(f"Admin user {admin_email} deleted successfully.")
        else:
            print(f"No admin user found with email: {admin_email}")

if len(sys.argv) > 1:
    if sys.argv[1] == '1':
        create_admin()
    elif sys.argv[1] == '2':
        delete_admin()
    else:
        print("Invalid argument. Use '1' to create admin and '2' to delete admin.")
else:
    print("Missing argument. Use '1' to create admin and '2' to delete admin.")
