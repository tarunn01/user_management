def test_register_and_login(manager):
    user = manager.register("john", "john@email.com", "pass123")
    assert user.username == "john"

    session = manager.login("john", "pass123")
    assert session.username == "john"

def test_permission_check(manager):
    manager.register("alice", "a@b.com", "123", role="user")
    session = manager.login("alice", "123")
    assert manager.has_permission(session.token, "view_profile")
    assert not manager.has_permission(session.token, "delete_user")

def test_password_reset(manager):
    manager.register("bob", "b@b.com", "abc")
    token = manager.request_password_reset("b@b.com")
    manager.reset_password(token, "newpass")
    # login should succeed with new password
    session = manager.login("bob", "newpass")
    assert session.username == "bob"
