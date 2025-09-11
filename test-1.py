import sqlalchemy
from sqlalchemy import select

print("Hello World!")


stmt = select(Dogs).where(name="Good Boy")