from app.schemas.user import UserCreate
from app.schemas.post import PostCreate

user = UserCreate(
    name="João",
    email="JOAO@email.com",
    password="senha123",
    role="contractor",
)

post = PostCreate(
    title="Desenvolvimento de API",
    description="Preciso de um profissional para desenvolver uma API.",
    category="Desenvolvimento",
    budget="1500.00",
)

print(user.model_dump_json(exclude={"password"}))
print(post.model_dump())