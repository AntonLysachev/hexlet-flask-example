import json


def user_save(user):
  bd = {}
  add_user = {}
  with open('resurses/user_bd.json', 'r') as rf:
    bd = json.load(rf)
  id = bd['id'] + 1
  add_user.update(bd)
  user['id'] = id
  add_user[id] = user
  add_user['id'] = id
  with open('resurses/user_bd.json', 'w') as wf:
    json.dump(add_user, wf, indent=2)


def user_save_cookie(user, cookie):
    users = {}
    if cookie:
        id = cookie["id"] + 1
        users.update(cookie)
    else:
        id = 1
    users["id"] = id
    user["id"] = id
    users[id] = user
    return json.dumps(users)


def email_save_cookie(email, cookie):
    if email in cookie:
        return json.dumps(cookie)
    else:
        cookie.append(email)
        return json.dumps(cookie)