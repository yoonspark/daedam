from config import ENTRIES_PER_PAGE

from models import Topic, Panelist


def paginate(request, entries: list) -> list:
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ENTRIES_PER_PAGE
    end = start + ENTRIES_PER_PAGE
    current_entries = entries[start:end]

    return current_entries


def get_topic(name: str):
    t = Topic.query.filter(Topic.name == name).first()
    if not t:
        t = Topic(name=name)

    return t


def get_panelist(name: str):
    p = Panelist.query.filter(Panelist.name == name).first()
    if not p:
        p = Panelist(name=name)

    return p
