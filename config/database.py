from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


DB_URL="postgresql://root:naLjElRI73WI6cCi5NSCio1M59793ro2@dpg-cn2fjhv109ks7396ajug-a.oregon-postgres.render.com/db_my_store_lb2z"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)



