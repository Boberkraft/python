from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, Column, Integer, String, DateTime, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import create_engine


engine = create_engine('sqlite:///database/local.db', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
backref('images', lazy='dynamic')

image_tags = Table('image_tags', Base.metadata,
                   Column('image_id', Integer, ForeignKey('images.id')),
                   Column('tag_id', Integer, ForeignKey('tag.id'))
                   )


class Selected(Base):
    __tablename__ = 'selected'

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    image = relationship('Image', backref=backref('image', uselist=False))


class Uploaded(Base):
    __tablename__ = 'uploaded'

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    image = relationship('Image', backref=backref('new', uselist=False))



class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    original_name = Column(String)
    uploader = Column(String)
    file = Column(String)
    add_date = Column(DateTime(timezone=True), default=func.now())
    modify_date = Column(DateTime(timezone=True), default=func.now())
    tags = relationship('Tag',
                        secondary=image_tags,
                        backref=backref('image', lazy='dynamic'))


    def __repr__(self):
        return '<Image(name={})>'.format(self.name)


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return '<Tag(name={})>'.format(self.name)


Base.metadata.create_all(engine)

# img = Image(name='Zenek')
# print(img)

class Database:
    Tag = Tag
    Image = Image
    Selected = Selected
    Uploaded = Uploaded
    session = Session()
    text = text


    @classmethod
    def commit(cls):
        cls.session.commit()
        # try:
        #     cls.session.commit()
        # except:
        #     print('ROLLBACKING AN ERROR OCCURRED!!!!!!!!!!!!!!!!!!!')
        #     cls.session.rollback()

    # session.add_all([...])
    # session.add(...)
    # session.commit()
    # session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
    # session.delete(jack)
    # our_user = session.query(User).filter_by(name='ed').first()

