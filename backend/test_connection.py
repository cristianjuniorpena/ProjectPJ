from sqlalchemy import text

from app.database.session import engine

try:
    with engine.connect() as connection:

        result = connection.execute(text("SELECT version()"))

        print("Conexão estabelecida!")

        print(result.scalar())

except Exception as error:
    print("Erro ao conectar com PostgreSQL:")
    print(error)

finally:
    engine.dispose()