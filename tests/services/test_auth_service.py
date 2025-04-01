from unittest.mock import MagicMock, patch

import pytest

from app.consts.Roles import RoleConsts
from app.consts.auth import AuthConsts
from app.models.response import ResponseModel
from app.service.authService import AuthService


class TestAuthService:
    @pytest.fixture
    def mock_user(self):
        user = MagicMock()
        user.user_id = 1
        user.username = "testuser"
        user.status = True
        user.check_password.return_value = True
        user.to_dict.return_value = {
            "user_id": 1,
            "username": "testuser",
            "email": "test@example.com"
        }
        return user

    @pytest.fixture
    def mock_role(self):
        role = MagicMock()
        role.role_id = 1
        role.name = RoleConsts.USER
        return role

    @patch('app.service.authService.create_access_token')
    @patch('app.service.authService.UserRolePermissionMapper')
    @patch('app.service.authService.UserMapper')
    def test_login_success(self, MockUserMapper, MockUserRolePermissionMapper, mock_create_token, mock_user, app):
        with app.app_context():
            # Setup mocks
            MockUserMapper.get_user_by_name.return_value = mock_user
            MockUserRolePermissionMapper.getUserRole.return_value = [{
                "role_id": 2,
                "role_name": "USER",
                "description": "一般用户"
            }]
            MockUserRolePermissionMapper.getRolePermissions.return_value = [{
                "permission_id": 1,
                "permission_name": "test_permission",
                "description": "测试权限"
            }]
            mock_create_token.return_value = "mock_access_token"

            # Call the function to test
            response = AuthService.login("testuser", "password123")

            # Assertions
            assert isinstance(response, ResponseModel)
            assert response.code == 0
            assert response.msg == AuthConsts.LOGIN_SUCCESS
            assert response.data["access_token"] == "mock_access_token"
            assert "payload" in response.data
            MockUserMapper.get_user_by_name.assert_called_once_with("testuser")
            mock_user.check_password.assert_called_once_with("password123")
            MockUserMapper.update_last_login.assert_called_once_with(mock_user.user_id)
            MockUserRolePermissionMapper.getUserRole.assert_called_once_with(mock_user.user_id)
            expected_payload = {
                "user": mock_user.to_dict(),
                "role": [{
                    "role_id": 2,
                    "role_name": "USER",
                    "description": "一般用户"
                }],
                "permissions": [{
                    "permission_id": 1,
                    "permission_name": "test_permission",
                    "description": "测试权限"
                }]
            }
            mock_create_token.assert_called_once()
            call_args = mock_create_token.call_args[1]
            assert call_args["identity"] == expected_payload

    @patch('app.service.authService.UserMapper')
    def test_login_invalid_credentials(self, MockUserMapper, mock_user, app):
        with app.app_context():
            # Setup mocks
            mock_user.check_password.return_value = False
            MockUserMapper.get_user_by_name.return_value = mock_user

            # Call the function to test
            response = AuthService.login("testuser", "wrongpassword")

            # Assertions
            assert response.code == 1
            assert response.msg == AuthConsts.LOGIN_ERROR

    @patch('app.service.authService.UserMapper')
    def test_login_user_not_found(self, MockUserMapper, app):
        with app.app_context():
            # Setup mocks
            MockUserMapper.get_user_by_name.return_value = None

            # Call the function to test
            response = AuthService.login("nonexistentuser", "password123")

            # Assertions
            assert response.code == 1
            assert response.msg == AuthConsts.LOGIN_ERROR

    @patch('app.service.authService.UserMapper')
    def test_login_disabled_account(self, MockUserMapper, mock_user, app):
        with app.app_context():
            # Setup mocks
            mock_user.status = False
            MockUserMapper.get_user_by_name.return_value = mock_user

            # Call the function to test
            response = AuthService.login("testuser", "password123")

            # Assertions
            assert response.code == 1
            assert response.msg == AuthConsts.ACCOUNT_DISABLED
