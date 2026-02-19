from werkzeug.security import check_password_hash


def authenticate_user(email, password, users):
    user = next((u for u in users if u["email"] == email), None)

    if user and check_password_hash(user["password"], password):
        return user

    return None