from app.schemas.auth import LoginResponse


class AuthService:
    def login(self, account: str, password: str) -> LoginResponse | None:
        if account == "teacher01" and password == "secret123":
            return LoginResponse(access_token="dev-token", role="teacher")
        if account == "student01" and password == "secret123":
            return LoginResponse(access_token="student-token", role="student")
        return None
