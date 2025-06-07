from app.__init__ import create_app
from app.models import db, Statistic

app = create_app()

with app.app_context():
    stat = db.session.get(Statistic, 2)
    if stat:
        stat.disagree_count += 1000000
        db.session.commit()
        print("| UPDATED |")
    else:
        print("| NOT FOUND |")