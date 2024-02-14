import json


def validate(user):
  errors = {}
  first_name = user['first_name']
  last_name = user['last_name']
  email = user['email']
  with open('resurses/user_bd.json', 'r') as rf:
    db = json.load(rf)
  db.pop('id')
  for user_data in db.values():
    if email == user_data['email']:
      errors['email'] = 'Такой email уже зарегестрирован'

  if first_name:
    if len(first_name) < 3:
       errors['first_name'] = 'Короткое имя'
  if last_name:
    if len(last_name) < 3:
      errors['last_name'] = 'Короткая фамилия'
  return errors


def validate_update(user):
  errors = {}
  first_name = user['first_name']
  last_name = user['last_name']

  if first_name:
    if len(first_name) < 3:
       errors['first_name'] = 'Короткое имя'
  if last_name:
    if len(last_name) < 3:
      errors['last_name'] = 'Короткая фамилия'
  return errors


def validate_email(email):
    errors = {}
    with open('resurses/user_bd.json', 'r') as rf:
        db = json.load(rf)
    db.pop('id')
    for user_data in db.values():
        if email in user_data['email']:
            break
    else:
        errors['email'] = 'Такой email не существует'
        return errors


def is_login(session, cookie):
    for email in cookie:
        if session[email]['login']:
          return True
    return False
   