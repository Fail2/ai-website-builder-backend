from app.core.model import get_structurer_model


def create_structurer(schema):
    return get_structurer_model().with_structured_output(
        schema,
        method="json_schema",
    )