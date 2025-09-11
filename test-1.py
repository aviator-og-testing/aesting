import sqlalchemy
from sqlalchemy import select

print("Hello World!")


dog = session.execute(select(Dogs).where(Dogs.name=="Good Boy")).scalars().first()