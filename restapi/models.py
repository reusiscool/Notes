from datetime import datetime

from .db import get_db


class User:
    def __init__(self, id_, username, password_hash):
        self._id = id_
        self._username = username
        self._password_hash = password_hash

    @staticmethod
    def register(username, password_hash):
        db = get_db()
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, password_hash),
            )
            db.commit()
        except db.IntegrityError:
            raise UserAlreadyExists()
        return User.with_username(username)

    def delete(self):
        notes = Note.with_author_id(self.id())
        for note in notes:
            note.delete_fr()
        db = get_db()
        db.execute(
            "DELETE FROM user WHERE id = ?",
            (self.id(),),
        )
        db.commit()

    def username(self):
        return self._username

    def password_hash(self):
        return self._password_hash

    def id(self):
        return self._id

    def to_json(self):
        return {
            'id': self._id,
            'username': self._username
        }

    def set_tg_id(self, id_):
        db = get_db()
        data = db.execute("Select * FROM telegram WHERE tg_id = ?", (id_,)).fetchone()
        if data is None:
            db.execute("INSERT INTO telegram (tg_id, user_id) VALUES (?, ?)", (id_, self.id()))
        else:
            db.execute("UPDATE telegram SET user_id = ? WHERE tg_id = ?", (self.id(), id_))
        db.commit()

    def set_password(self, password_hash):
        db = get_db()
        db.execute("UPDATE user SET password = ? WHERE id = ?", (password_hash, self.id()))
        db.commit()

    def get_tg(self) -> list[int]:
        db = get_db()
        data = db.execute("SELECT tg_id FROM telegram WHERE user_id = ?", (self.id(),)).fetchall()
        return [i['tg_id'] for i in data]

    @staticmethod
    def with_id(id_):
        data = get_db().execute("SELECT id, username, password FROM user WHERE id = ?", (id_,)).fetchone()
        if data is None:
            return None
        return User(data["id"], data["username"], data["password"])

    @staticmethod
    def with_username(username):
        data = get_db().execute("SELECT id, username, password FROM user WHERE username = ?", (username,)).fetchone()
        if data is None:
            return None
        return User(data["id"], data["username"], data["password"])

    @staticmethod
    def with_telegram_id(id_):
        db = get_db()
        data = db.execute("SELECT user_id FROM telegram WHERE tg_id = ?", (id_,)).fetchone()
        if data is None:
            return None
        return User.with_id(data[0])

    @staticmethod
    def reset_tg_id(tg_id):
        db = get_db()
        db.execute("DELETE FROM telegram WHERE tg_id = ?", (tg_id,))
        db.commit()


class UserAlreadyExists(Exception):
    pass


class Note:
    def __init__(self, id_, title, body, author, created, deleted, notify):
        self._id = id_
        self._title = title
        self._body = body
        self._author = author
        self._created = created
        self._deleted = deleted
        self._notify = notify

    @staticmethod
    def create(title, body, author_id, notification=None):
        db = get_db()
        if notification == '':
            notification = None
        else:
            notification = datetime.strptime(notification, '%Y-%m-%dT%H:%M')
        db.execute(
            "INSERT INTO post (title, body, author_id, notify) VALUES (?, ?, ?, ?)",
            (title, body, author_id, notification),
        )
        db.commit()

    def update(self, title, body):
        db = get_db()
        db.execute(
            "UPDATE post SET title = ?, body = ? WHERE id = ?",
            (title, body, self.id())
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("UPDATE post SET deleted = CURRENT_TIMESTAMP WHERE id = ?", (self.id(),))
        db.commit()

    def delete_fr(self):
        db = get_db()
        db.execute("DELETE FROM post WHERE id = ?", (self.id(),))
        db.commit()

    def restore(self):
        if not self.is_deleted():
            raise RuntimeError(f'{self._id} note is not deleted')
        db = get_db()
        db.execute("UPDATE post SET deleted = NULL, created = ? WHERE id = ?", (self._deleted, self.id()))
        db.commit()

    def id(self):
        return self._id

    def notify(self):
        return self._notify

    def title(self):
        return self._title

    def body(self):
        return self._body

    def author(self):
        return self._author

    def created(self):
        return self._created

    def deleted(self):
        return self._deleted

    def is_deleted(self):
        return self._deleted is not None

    def to_json(self):
        return {'id': self.id(), 'body': self.body(), 'author_id': self.author().id(),
                'title': self.title(), 'created': self.created(), 'notify': self.notify(), 'deleted': self.deleted()}

    @staticmethod
    def all():
        posts = get_db().execute(
            "SELECT id, title, body, created, author_id, deleted, notify"
            " FROM post ORDER BY created DESC"
        ).fetchall()
        return [Note(p["id"], p["title"], p["body"], User.with_id(p["author_id"]),
                     p["created"], p['deleted'], p['notify'])
                for p in posts]

    @staticmethod
    def all_on_time():
        db = get_db()
        posts = db.execute("SELECT id FROM post WHERE notify IS NOT NULL "
                           "AND notify < CURRENT_TIMESTAMP").fetchall()
        for p in posts:
            db.execute('UPDATE post SET notify = NULL WHERE id = ?', (p['id'],))
            db.commit()
        return [Note.with_id(p['id']) for p in posts]

    @staticmethod
    def with_author_id(author_id):
        posts = get_db().execute(
            "SELECT id, title, body, created, author_id, deleted, notify"
            " FROM post WHERE author_id = ? ORDER BY created DESC", (author_id,)
        ).fetchall()
        return [Note(p["id"], p["title"], p["body"], User.with_id(p["author_id"]),
                     p["created"], p['deleted'], p['notify'])
                for p in posts]

    @staticmethod
    def with_id(id_):
        data = get_db().execute(
            "SELECT id, title, body, created, author_id, deleted, notify"
            " FROM post WHERE id = ?", (id_,)).fetchone()
        if data is None:
            return None
        return Note(data["id"], data["title"], data["body"],
                    User.with_id(data["author_id"]), data["created"], data['deleted'], data["notify"])
