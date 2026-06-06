import hashlib
from .models import UserInDB, WorldCupCategory, WorldCupItem

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# 인메모리 DB (실제 프로덕션에서는 RDS/DynamoDB 등으로 교체)
_users: list[UserInDB] = [
    UserInDB(id=1, username="admin", hashed_password=_hash("admin1234"), role="admin"),
    UserInDB(id=2, username="user1", hashed_password=_hash("user1234"),  role="user"),
]

_categories: list[WorldCupCategory] = [
    WorldCupCategory(id=1, name="음식", emoji="🍔", active=True, items=[
        WorldCupItem(id=i, name=n, emoji=e, category_id=1)
        for i, (n, e) in enumerate([
            ("피자","🍕"),("치킨","🍗"),("햄버거","🍔"),("삼겹살","🥩"),
            ("라면","🍜"),("초밥","🍣"),("떡볶이","🌶️"),("파스타","🍝"),
        ], 1)
    ]),
    WorldCupCategory(id=2, name="여행지", emoji="✈️", active=True, items=[
        WorldCupItem(id=i, name=n, emoji=e, category_id=2)
        for i, (n, e) in enumerate([
            ("제주도","🏝️"),("도쿄","🗼"),("파리","🗼"),("뉴욕","🗽"),
            ("발리","🌴"),("런던","🎡"),("방콕","🛕"),("시드니","🦘"),
        ], 9)
    ]),
]

def get_user(username: str) -> UserInDB | None:
    return next((u for u in _users if u.username == username), None)

def verify_password(plain: str, hashed: str) -> bool:
    return _hash(plain) == hashed

def get_categories() -> list[WorldCupCategory]:
    return _categories
