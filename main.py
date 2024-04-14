from sqlalchemy import create_engine, ForeignKey, String, Column
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Users(Base):
    __tablename__ = "users"
    user_id = Column("userId", String, primary_key=True, default=generate_uuid)
    first_name = Column("firstName", String)
    last_name = Column("lastName", String)
    profile_name = Column("profileName", String)
    email = Column("email", String)

    def __init__(self, first_name, last_name, profile_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.profile_name = profile_name
        self.email = email


class Posts(Base):
    __tablename__ = "posts"
    post_id = Column("postId", String, primary_key=True, default=generate_uuid)
    user_id = Column("userId", String, ForeignKey("users.user_id"))
    post_content = Column("postContent", String)

    def __init__(self, user_id, post_content):
        self.user_idd = user_id
        self.post_content = post_content


class Likes(Base):
    __tablename__ = "likes"
    likeId = Column("likeId", String, primary_key=True, default=generate_uuid)
    userId = Column("userId", String, ForeignKey("users.user_id"))
    postId = Column("postId", String, ForeignKey("posts.post_id"))

    def __init__(self, user_id, post_id):
        self.userId = user_id
        self.postId = post_id


db = "sqlite:///socialDB.db"
engine = create_engine(db)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_user(session, first_name, last_name, profile_name, email):
    # filter emails, check if the email exists in db
    exist = session.query(Users).filter(Users.email == email).all()
    if len(exist) > 0:
        print("Email address already exists.")
    else:
        user = Users(first_name, last_name, profile_name, email)
        session.add(user)
        session.commit()
        print("User added.")


def add_post(session, user_id, post_content):
    post = Posts(user_id, post_content)
    session.add(post)
    session.commit()
    print("Post added.")


def add_like(session, user_id, post_id):
    like = Likes(user_id, post_id)
    session.add(like)
    session.commit()
    print("Like added.")


