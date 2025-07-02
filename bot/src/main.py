import os
from flask import Flask, jsonify
from flask_cors import CORS
from src.models.conversation import db
from src.routes.whatsapp import whatsapp_bp

app = Flask(__name__)
CORS(app)

# Configurações
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dentinhos-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dentinhos_bot.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Corrigir URL do PostgreSQL no Heroku se necessário
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://')

# Inicializar banco de dados
db.init_app(app)

# Registrar blueprints
app.register_blueprint(whatsapp_bp, url_prefix='/api/whatsapp')

@app.route('/')
def home():
    return jsonify({
        "message": "Bot WhatsApp Dentinhos de Leite Odontologia",
        "status": "online",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

