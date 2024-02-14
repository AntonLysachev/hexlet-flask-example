import json


def user_update(update_db):
  with open('resurses/user_bd.json', 'r') as rf:
    db = json.load(rf)
  db.update(update_db)
  with open('resurses/user_bd.json', 'w') as wf:
    json.dump(db, wf, indent=2)
