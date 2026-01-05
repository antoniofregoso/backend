from fastapi import HTTPException
from passlib.context import CryptContext

from Models.user import User
from Repository.user import UserRepository
from schema import RegisterInput, LoginInput, LoginType
from Middleware.JWTManager import JWTManager

class AuthenticationService:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return AuthenticationService.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def login(login: LoginInput):
        existing_user = await UserRepository.get_by_email(login.email)

        if not existing_user:
            raise HTTPException(status_code=401, detail="Email not found!")

        if not AuthenticationService.verify_password(login.password, existing_user.password):
            raise HTTPException(status_code=401, detail="Incorrect password!")

        token = JWTManager.generate_token({"sub": existing_user.email})

        return LoginType(email=existing_user.email, token=token)

    @staticmethod
    async def register(user: RegisterInput):
        existing_user = await UserRepository.get_by_email(user.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = AuthenticationService.pwd_context.hash(user.password)
        new_user = User(name=user.name, email=user.email, password=hashed_password)
        await UserRepository.create(new_user)

        return "User registered successfully"

        