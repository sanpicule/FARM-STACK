import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config

# 環境変数に格納されている変数を呼び出す
JWT_KEY=config('JWT_KEY')

class AuthJwtCsrf():
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = JWT_KEY

    def generate_hashed_pw(self, password) -> str:
        return self.pwd_ctx.hash(password)
    
    def verify_pw(self, plan_pw, hashed_pw) -> bool:
        return self.pwd_ctx.verify(plan_pw, hashed_pw)
    
    def encode_jwt(self, email) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm='HS256'
        )


    def decode_jwt(self, token) -> str:
        try:
            # エラーが起きそうな処理をここに記載する
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload(['sub'])
        # 実際のエラー内容をここに記載
        except jwt.ExpiredSignatureError:
            # raiseで例外を発生させ処理を止める
            raise HTTPException(
                status_code=401, detail='The JWT has expired'
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='JWT is not valid')