from CRUD.crud_utils import get_column, get_field, get_table, save, delete, update, get_user


# user_id = get_column('id', 'users', 'email', 'anton@mail.ru')
# print(user_id)
user = get_field('users', 'id', 4)
print(user)