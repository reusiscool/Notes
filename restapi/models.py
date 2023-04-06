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
        # todo
        # db.execute("DELETE FROM telegram WHERE user_id = ?", (self.id()))
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


class UserAlreadyExists(Exception):
    pass


class Note:
    def __init__(self, id_, title, body, author, created, deleted):
        self._id = id_
        self._title = title
        self._body = body
        self._author = author
        self._created = created
        self._deleted = deleted

    @staticmethod
    def create(title, body, author_id):
        db = get_db()
        db.execute(
            "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
            (title, body, author_id),
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

    @staticmethod
    def all():
        posts = get_db().execute(
            "SELECT id, title, body, created, author_id, deleted"
            " FROM post ORDER BY created DESC"
        ).fetchall()
        return [Note(p["id"], p["title"], p["body"], User.with_id(p["author_id"]), p["created"], p['deleted'])
                for p in posts]

    @staticmethod
    def with_author_id(author_id):
        posts = get_db().execute(
            "SELECT id, title, body, created, author_id, deleted"
            " FROM post WHERE author_id = ? ORDER BY created DESC", (author_id,)
        ).fetchall()
        return [Note(p["id"], p["title"], p["body"], User.with_id(p["author_id"]), p["created"], p['deleted'])
                for p in posts]

    @staticmethod
    def with_id(id_):
        data = get_db().execute(
            "SELECT id, title, body, created, author_id, deleted"
            " FROM post WHERE id = ?", (id_,)).fetchone()
        if data is None:
            return None
        return Note(data["id"], data["title"], data["body"],
                    User.with_id(data["author_id"]), data["created"], data['deleted'])
