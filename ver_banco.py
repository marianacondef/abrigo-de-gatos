from app import create_app, db

app = create_app()

with app.app_context():
    print("Banco de dados em uso:")
    print(db.engine.url)
