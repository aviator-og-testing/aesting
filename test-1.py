import sqlalchemy

print("Hello World!")


dog = session.execute(select(Dogs).where(name="Good Boy")).scalars().first()