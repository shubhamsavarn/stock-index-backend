from app.repos.composition_repo import CompositionRepository


class CompositionError(Exception):
    pass


def get_composition(date: str):
    try:
        return CompositionRepository.get_composition_by_date(date)
    except Exception as e:
        raise CompositionError(str(e))


def get_composition_changes(start_date: str, end_date: str):
    try:
        return CompositionRepository.get_composition_changes(start_date, end_date)
    except Exception as e:
        raise CompositionError(str(e))
