from models.user import User


def test_create_user():
    user = User(
        "Alex",
        "alex@gmail.com"
    )

    assert user.name == "Alex"
    assert user.email == "alex@gmail.com"