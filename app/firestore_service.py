import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


project_id = 'platzi-flask-2....'
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})


db = firestore.client()


def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection("users").document(user_id).get()

def user_put(user_data):
    user_ref = db.collection("users").add(user_data.username)
    user_ref.set({ "password": user_data.password})

def get_todos(user_id):
    return db.collection("users").get(user_id)

def put_todo(user_id, description):
    todo_collection_ref = db.collection("users").documenmt(user_id).collection("todos")
    todo_collection_ref.add({"description": description})


def delete_todo(user_id, todo_id):
    todo_ref = db.document(f'users/{user_id}/todos/{todo_id}')
    todo_ref.delete()


def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({"done": todo_done})


def _get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')
