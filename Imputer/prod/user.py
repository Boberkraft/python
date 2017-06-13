from database import Database
from singleton import Singleton
import os

class User:

    @staticmethod
    def unselect(id=None):
        if id is None:
            # delete all records
            Database.session.query(Database.Selected).delete()
        else:
            # delete specified id
            Database.session.query(Database.Selected).filter_by(image_id=id).delete()
        Database.commit()

    @staticmethod
    def select(id=None):
        exist = Database.session.query(Database.Selected).filter_by(image_id=id).first()
        if not exist:
            if id is None:
                pass
            else:
                selected = Database.Selected(image_id=id)
                Database.session.add(selected)
            Database.commit()
        else:
            print('This image is already selected')

    @staticmethod
    def delete_selected():
        Database.session.query(Database.Image).delete()
        Database.commit()

    @staticmethod
    def get_selected():
        return Database.session.query(Database.Image).join(Database.Selected)

    @staticmethod
    def add_uploaded(id, tags):
        Database.session.query(Database.Uploaded).filter_by(image_id=id).delete()
        img = Database.session.query(Database.Image).filter_by(id=id).first()
        print(img)
        for tag in tags.split(','):
            tag = tag.strip().lower()
            if tag:
                if not Database.session.query(Database.Tag).filter_by(name=tag).first():
                    # tag not found
                    Database.session.add(Database.Tag(name=tag))
                    print('Creating new tag:', tag)
                database_tag = Database.session.query(Database.Tag).filter_by(name=tag).first()
                print('SELECTED TAG!!!!!!!!!!!',database_tag)
                img.tags.append(database_tag)
        Database.commit()

    @staticmethod
    def get_uploaded():
        return (Database.session.query(Database.Image)
                .join(Database.Uploaded))

    @staticmethod
    def delete(id):
        print('DELETED IMAGE WITH ID =', id)
        Database.session.query(Database.Uploaded).filter_by(image_id=id).delete()
        img = Database.session.query(Database.Image).filter_by(id=id).first()
        try:
            path = os.path.join('uploads', img.file)
            os.remove(path)  # remove file
        except FileNotFoundError:
            print('File {} not found'.format(path))
        Database.session.delete(img)
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
        Database.session.add_all(new_images)
        Database.session.add_all(uploaded)

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