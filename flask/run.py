from app import create_app, db
import sys
import click

app = create_app()

@app.cli.command("create_db")
def create_db():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
        click.echo("Database tables created.")
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
