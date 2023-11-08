import os
import talisker.requests

# Packages
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.discourse import (
    Docs,
    DiscourseAPI,
    DocParser,
)
from canonicalwebteam.search import build_search_view
from flask import render_template, make_response

# TODO: make this a configuration parameter on flask-base
os.environ["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]

app = FlaskBase(
    __name__,
    "dqlite.io",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)
session = talisker.requests.get_session()

docs_url_prefix = "/docs"
discourse_docs = Docs(
    parser=DocParser(
        api=DiscourseAPI(
            base_url="https://discourse.dqlite.io/",
            session=session,
        ),
        index_topic_id=34,
        url_prefix=docs_url_prefix,
    ),
    document_template="docs/document.html",
    url_prefix=docs_url_prefix,
)

app.add_url_rule(
    "/docs/search",
    "docs-search",
    build_search_view(
        session=session,
        site="https://dqlite.io/docs",
        template_path="docs/search.html",
    ),
)

discourse_docs.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sitemap.xml")
def sitemap_index():
    xml_sitemap = render_template("sitemap/sitemap-index.xml")
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route("/sitemap-links.xml")
def sitemap_links():
    xml_sitemap = render_template("sitemap/sitemap-links.xml")
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response
