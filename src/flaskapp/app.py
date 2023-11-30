from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskapp.routes import (
    DownloadView,
    IndexView,
    AddBookView,
    AddArticleView,
    ListView,
)
from flaskapp.validator import EntryValidator
from repositories.citation_repository import CitationRepository
from services.citation_service import CitationService
from bibtex.bibtex_creator import BibteXExporter

# from sqlalchemy.sql import text

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"

app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")


db = SQLAlchemy(app)
db_relay = CitationRepository(db)

citation_service = CitationService(db_relay)

bibtex_exporter = BibteXExporter()

app.add_url_rule(
    "/",
    view_func=IndexView.as_view("index", "index.html"),
)

app.add_url_rule(
    "/add_new_book",
    view_func=AddBookView.as_view(
        "add_new_book", citation_service, EntryValidator(), "add_new_book.html"
    ),
)

app.add_url_rule(
    "/add_new_article",
    view_func=AddArticleView.as_view(
        "add_new_article", citation_service, EntryValidator(), "add_new_article.html"
    ),
)

app.add_url_rule(
    "/list",
    view_func=ListView.as_view("list", citation_service, "list.html"),
)

app.add_url_rule(
    "/download",
    view_func=DownloadView.as_view("download", citation_service, bibtex_exporter)
)
