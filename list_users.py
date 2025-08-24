from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("📊 пользователи в системе:")
    for user in users:
        print(f"  {user.id}: {user.username} ({user.role}) - {user.email}")
    print(f"всего пользователей: {len(users)}")
