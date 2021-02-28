import pytest

from unittest.mock import patch

from freezegun import freeze_time

from amazon_killer import app, UserAPI, CartAPI


@pytest.fixture
def store_app():
    app.config['TESTING'] = True
    with app.test_client() as client:
        return client


@freeze_time('2021-02-08 14:16:41')
@patch.dict(UserAPI.USERS_DATABASE, {}, clear=True)
def test_create_user(store_app):
    response = store_app.post(
        '/users',
        json={
            "name": "Illia",
            "email": "illia.sukonnik@gmail.com",
        })
    assert response.status_code == 201
    assert response.json == {
        "user_id": 1,
        "registration_timestamp": '2021-02-08T14:16:41'
    }
    user_id = response.json['user_id']
    response = store_app.get(f'/users/{user_id}')

    assert response.status_code == 200
    assert response.json == {
        "name": "Illia",
        "email": "illia.sukonnik@gmail.com",
        "user_id": user_id,
        "registration_timestamp": '2021-02-08T14:16:41',
    }


@patch.dict(UserAPI.USERS_DATABASE, {}, clear=True)
def test_get_user_no_such_user(store_app):
    response = store_app.get('/users/2')

    assert response.status_code == 404
    assert response.json == {
        "error": "no such user with id=2"}


@patch.dict(UserAPI.USERS_DATABASE, {1: {
    "name": "Illia",
    "email": "illia.sukonnik@gmail.com",
    "user_id": 1}}, clear=True)
def test_set_user(store_app):
    response = store_app.put(
        '/users/1',
        json={
            "name": "Illia",
            "email": "illia.sukonnik@example.com",
        }
    )

    assert response.status_code == 200

    response = store_app.put(
        '/users/3',
        json={
            "name": "Illia",
            "email": "illia.sukonnik@example.com",
        }
    )

    assert response.status_code == 404
    assert response.json == {
        "error": "no such user with id=3"
    }


@patch.dict(UserAPI.USERS_DATABASE, {1: {
    "name": "Illia",
    "email": "illia.sukonnik@gmail.com",
    "user_id": 1}}, clear=True)
def test_remove_user(store_app):
    response = store_app.delete('/users/1')

    assert response.status_code == 200

    response = store_app.delete('/users/3')

    assert response.status_code == 404
    assert response.json == {
        "error": "no such user with id=3"
    }


@freeze_time('2021-02-08 14:16:41')
@patch.dict(UserAPI.USERS_DATABASE, {1: {
    "name": "Illia",
    "email": "illia.sukonnik@gmail.com",
    "user_id": 1}}, clear=True)
@patch.dict(CartAPI.CARTS_DATABASE, {1: {
    "products": {"product": "book",
                 "price": 500},
    "cart_id": 1}}, clear=True)
def test_create_cart(store_app):
    response = store_app.post(
        '/carts',
        json={
            "user_id": 1,
            "products": [
                {
                    "product": 'Book: how to stop be boring',
                    "price": 500,
                },
                {
                    "product": 'fireworks',
                    "price": 1500,
                }
            ]
        }
    )
    assert response.status_code == 201
    assert response.json == {
        "cart_id": 1,
        "creation_time": '2021-02-08T14:16:41'
    }

    cart_id = response.json['cart_id']
    response = store_app.get(f'/carts/{cart_id}')

    assert response.status_code == 200
    assert response.json == {
        "cart_id": cart_id,
        "user_id": 1,
        "creation_time": '2021-02-08T14:16:41',
        "products": [
            {
                "product": 'Book: how to stop be boring',
                "price": 500,
            },
            {
                "product": 'fireworks',
                "price": 1500,
            }
        ]
    }


@patch.dict(CartAPI.CARTS_DATABASE, {}, clear=True)
def test_get_cart_no_such_cart(store_app):
    response = store_app.get('/carts/2')

    assert response.status_code == 404
    assert response.json == {
        "error": "no such cart with id=2"
    }


@patch.dict(UserAPI.USERS_DATABASE, {1: {
    "name": "Illia",
    "email": "illia.sukonnik@gmail.com",
    "user_id": 1}}, clear=True)
@patch.dict(CartAPI.CARTS_DATABASE, {1: {
    "products": {"product": "book",
                 "price": 500},
    "cart_id": 1}}, clear=True)
def test_set_cart(store_app):
    response = store_app.put(
        '/carts/1',
        json={
            "user_id": 1,
            "products": [
                {
                    "product": 'fireworks',
                    "price": 1500,
                }
            ]
        }
    )

    assert response.status_code == 200

    response = store_app.put(
        '/carts/3',
        json={
            "user_id": 1,
            "products": [
                {
                    "product": 'fireworks',
                    "price": 1500,
                }
            ]
        }
    )

    assert response.status_code == 404
    assert response.json == {
        "error": "no such cart with id=3"
    }

    response = store_app.put(
        '/carts/1',
        json={
            "user_id": 3,
            "products": [
                {
                    "product": 'fireworks',
                    "price": 1500,
                }
            ]
        }
    )
    assert response.status_code == 404
    assert response.json == {
        "error": "no such user with id=3"
    }


@patch.dict(UserAPI.USERS_DATABASE, {1: {
    "name": "Illia",
    "email": "illia.sukonnik@gmail.com",
    "user_id": 1}}, clear=True)
@patch.dict(CartAPI.CARTS_DATABASE, {1: {
    "products": {"product": "book",
                 "price": 500},
    "cart_id": 1}}, clear=True)
def test_remove_cart(store_app):
    response = store_app.delete('/carts/1')

    assert response.status_code == 200

    response = store_app.delete('/carts/3')

    assert response.status_code == 404
    assert response.json == {
        "error": "no such cart with id=3"
    }
