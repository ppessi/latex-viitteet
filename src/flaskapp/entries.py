#import app
from sqlalchemy.sql import text

class Database():
    def __init__(self, db) -> None:
        self._db = db

    def add_book(self, authors, title, publisher, year):
        try:
            sql = text("INSERT INTO citations (title,publisher,year) \
                 VALUES (:title, :publisher, :year) RETURNING id")
            citation_id = self._db.session.execute(sql, {"title":title, "publisher":publisher,\
                 "year":year}).fetchone()[0]
            author_ids = []
            for author in authors.splitlines():
                author_ids.append(self._add_author(author))
            for author_id in author_ids:
                self._add_author_citation(author_id, citation_id)
            self._db.session.commit()
        except: #tää pitäis määritellä, lint: "No exception type(s) specified (bare-except)"
            return False
        return True

    def _add_author(self, name):
        sql = text("INSERT INTO authors (name) VALUES (:name) ON CONFLICT DO NOTHING")
        self._db.session.execute(sql, {"name": name})
        self._db.session.commit()
        sql = text("SELECT id FROM authors WHERE name = :name")
        result = self._db.session.execute(sql, {"name":name}).fetchone()[0]
        return result

    def _add_author_citation(self, author_id,citation_id):
        sql = text("INSERT INTO authors_citations (author_id, citation_id) \
            VALUES (:author_id, :citation_id)")
        self._db.session.execute(sql, {"author_id":author_id, "citation_id":citation_id})
        #app.db.session.commit()

    def get_all_citations(self):
        sql = text("SELECT * FROM citations")
        result = self._db.session.execute(sql).fetchall()
        return result

