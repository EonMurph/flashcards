from genanki import Note

class CustomNote(Note):
    """
    Custom Note class to add an attribute to the base Note.
    """
    def __init__(self, model=None, fields=None, sort_field=None, tags=None, guid=None, due=0) -> None:
        super().__init__(model=model, sort_field=sort_field, tags=tags, guid=guid, due=due)
        self.fieldData = fields
        if all(arg is not None for arg in [model, fields]):
            self.fields: dict[str, str] = {self.model.fields[i]["name"]: self.fieldData[i] for i in range(min(len(fields), len(model.fields)))}