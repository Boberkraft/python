from database import Database
from singleton import Singleton

class User:

    @staticmethod
    def unselect(id=None):
        if id is None:
            # delete all records
            Database.session.query(Database.Selected).delete()
        else:
            # delete specified id
            Database.session.query(Database.Selected).filter_by(id=id).delete()
        Database.commit()

    @staticmethod
    def select(images):
        new_images = []
        for img in images:
            # kword unpacking might me risky. Should i do it?
            new_image = Database.Image(name=img['name'],
                                       original_name=img['original_name'],
                                       file=img['file'])
            for tag in img['tags']:
                # add all the tags
                tag = Database.session.query(Database.Tag).filter_by(name=tag)
                new_image.tags.append(tag)
            new_images.append(new_image)
        Database.session.add_all(new_images)
        Database.commit()

    @staticmethod
    def delete_selected():
        Database.session.query(Database.Image).delete()
        Database.commit()

    @staticmethod
    def add_selected():
        Database.session.query(Database.Image).join(Database.Selected).all()
        Database.commit()

    @staticmethod
    def upload(images):
        new_images = []
        uploaded = []
        for img in images:
            # kword unpacking might me risky. Should i do it?
            new_image = Database.Image(name=img['name'],
                                       original_name=img['original_name'],
                                       file=img['file'])
            new_images.append(new_image)
            # add it to uploaded database
            upload = Database.Uploaded(image=new_image)
            uploaded.append(upload)
            new_images.append(new_image)
        Database.session.add_all(new_images)
        Database.session.add_all(uploaded)
        print('uploaded images!!')
        Database.commit()
        return [image.id for image in new_images]

    @staticmethod
    def get_images():

        return (Database.session.query(Database.Image)
              .outerjoin(Database.Uploaded)
              .filter(Database.Uploaded.id == None))

if __name__ == '__main__':
    x = User()
    x.unselect(1)


# Get commong
# SELECT * FROM selected
# INNER JOIN images
# ON images.id = selected.image_id

# Get this in Images that are not in Selected
# SELECT *
# FROM images A
# LEFT JOIN selected B
# ON A.id = B.image_id
# WHERE B.image_id IS NULL