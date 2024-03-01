from app.models import User
import json

def test_create_user(client, app):
    # Make a POST request to /api/users with JSON data
    response = client.post(
        '/api/users',
        data=json.dumps({
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }),
        content_type='application/json'
    )

    # Check that the response status code is 201 (Created)
    assert response.status_code == 201

    # Check that the user was created and returned in the response
    data = json.loads(response.get_data(as_text=True))
    assert data['name'] == 'John Doe'
    assert data['email'] == 'johndoe@example.com'

    with app.app_context():
        db_user = User.query.filter_by(email='johndoe@example.com').first()
        assert db_user is not None
        assert db_user.name == 'John Doe'
        assert db_user.email == 'johndoe@example.com'

def test_get_users(client, app, test_users):
    # Make a post request to /api/users with JSON data
    response = client.get('/api/users')
    # Check that the response status code is 200
    assert response.status_code == 200
    # Check that the response contains the right number of users
    response_users = json.loads(response.get_data(as_text=True))
    # Check that the last user in the response has the correct fields
    with app.app_context():
        db_users = User.query.all()
        assert len(db_users) > 0
        assert len(response_users) == len(db_users)
        for user in response_users:
            assert User.query.filter_by(name=user['name']).first() is not None
            assert User.query.filter_by(email=user['email']).first() is not None

def test_get_specific_user(client, app, test_users):
    # Make a post request to /api/users with JSON data
    response = client.get('/api/users/1')

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check for correct response
    response_user = json.loads(response.get_data(as_text=True))
    assert response_user['id'] == 1

    with app.app_context():
        db_user = User.query.get(1)
        assert db_user.name == response_user['name']
        assert db_user.email == response_user['email']

def test_get_non_existent_user(client, app, test_users):
    # Make a post request to /api/users with JSON data
    response = client.get('/api/users/100')

    # Check that the response status code is 404
    assert response.status_code == 404

    # Check for correct response
    response_user = json.loads(response.get_data(as_text=True))
    assert response_user['message'] == 'User with id 100 not found'
