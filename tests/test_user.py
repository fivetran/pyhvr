import pytest
import pyhvr
from pyhvr.pyhvr_exceptions import RestError

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234", uri="http://localhost:4340"
)


def test_get_users():
    users = hvr_client.get_users()
    assert users["admin"]["authentication"] == "local"


def test_get_users_props():
    user_prop = hvr_client.get_users_props(user="admin")
    assert user_prop["Full_Name"] == "Admin User"


def test_post_create_users():
    c_user = hvr_client.post_users(user="test_user1",
                                   authentication="local",
                                   password="welcome123",
                                   props={
                                       "Full_Name": "TestUser Name"
                                   }
                                   )
    assert c_user is None


def test_created_user():
    c_users = hvr_client.get_users_props(user="test_user1")
    assert c_users["Full_Name"] == "TestUser Name"


def wrong_user():
    try:
        hvr_client.get_users_user(user="test1_user1")
    except RestError as e:
        # test access to the fields
        print(e.status_code)
        print(e.message)
        print(e.error_code)


def test_patch_user_props():
    pl = {"Full_Name": "CFUser2"}
    ch_user = hvr_client.patch_users_props(user="test_user1", **pl)
    assert ch_user is None


def test_reset_user_password():
    up = hvr_client.put_users_password(user="test_user1", new_password="newpassword", current_password="welcome123")
    assert up is None


def test_delete_user():
    du = hvr_client.delete_users(user="test_user1")
    assert du is None


def test_non_user():
    with pytest.raises(RestError):
        hvr_client.delete_users(user="nouser")
