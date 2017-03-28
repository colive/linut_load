import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
conf_file='load_data.ini'
cf = ConfigParser.ConfigParser()
cf.read(conf_file)
host = cf.get("mysql", "host")
user = cf.get("mysql", "user")
passwd = cf.get("mysql", "password")
port = int(cf.getint("mysql", "port"))
db = cf.get("mysql", "db")
conn="mysql+mysqldb://%s:%s@%s/%s" % (user,passwd,host,db)
print conn
engine = create_engine(conn, convert_unicode=True) 
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
