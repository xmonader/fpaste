from models import *
from faker import Faker

fake = Faker()


def do_fixtures():
    for i in range(5):
        u1 = User(username=fake.first_name(),
                  email=fake.email(), password=fake.password())
        u2 = User(username=fake.first_name(),
                  email=fake.email(), password=fake.password())
        db.session.add(u1)
        db.session.add(u2)
        t = Tag(tag=fake.word())
        for x in range(3):
            p1 = Paste(title=fake.sentence(3), code=fake.paragraph(),
                       language=fake.language_code(), )
            p2 = Paste(title=fake.sentence(3), code=fake.paragraph(),
                       language=fake.language_code(),)
            p3 = Paste(title=fake.sentence(3), code=fake.paragraph(),
                       language=fake.language_code(),)
            db.session.add(p1)
            db.session.add(p2)
            db.session.add(p3)
            u1.pastes = [p1, p2]
            u2.pastes = [p3]
            t.pastes.extend([p1, p2, p3])
        db.session.add(t)
    db.session.commit()
