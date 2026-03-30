from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt, json

from models import db, User, Dataset
from generator import generate_dataset

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["JWT_SECRET_KEY"] = "secret"

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()

    user = User(username=data["username"], password=hashed)
    db.session.add(user)
    db.session.commit()

    return {"msg": "User created"}

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        return {"error": "User not found"}, 404

    if bcrypt.checkpw(data["password"].encode(), user.password.encode()):
        token = create_access_token(identity=user.id)
        return {"token": token}

    return {"error": "Invalid credentials"}, 401

# GENERATE
@app.route("/generate", methods=["POST"])
@jwt_required()
def generate():
    user_id = get_jwt_identity()

    dataset = generate_dataset({}, 5)

    db.session.add(Dataset(
        user_id=user_id,
        name="Dataset",
        data=json.dumps(dataset)
    ))
    db.session.commit()

    return jsonify(dataset)

# GET DATASETS
@app.route("/datasets", methods=["GET"])
@jwt_required()
def get_datasets():
    user_id = get_jwt_identity()

    datasets = Dataset.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "data": json.loads(d.data)
        }
        for d in datasets
    ])

# DELETE
@app.route("/datasets/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_dataset(id):
    user_id = get_jwt_identity()

    d = Dataset.query.filter_by(id=id, user_id=user_id).first()
    if not d:
        return {"error": "Not found"}, 404

    db.session.delete(d)
    db.session.commit()
    return {"msg": "Deleted"}

if __name__ == "__main__":
    app.run(debug=True)
