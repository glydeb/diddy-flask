def test_user_creation(app, test_user):
    assert test_user.name == 'John Doe'
    assert test_user.email == 'johndoe@example.com'
