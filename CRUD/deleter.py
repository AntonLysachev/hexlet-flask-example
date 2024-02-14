import json


def user_delete(id):
  with open('resurses/user_bd.json', 'r') as rf:
    db = json.load(rf)
  db.pop(id)
  with open('resurses/user_bd.json', 'w') as wf:
    json.dump(db, wf, indent=2)
