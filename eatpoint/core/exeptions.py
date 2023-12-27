class EventHasNoSeriaException(Exception):
    """Ошибка при попытке работы с серией события, когда событие разовое."""

    def __init__(self, message="Событие разовое и не имеет серии"):
        self.message = message
        super().__init__(message)


class SuchEventExistsException(Exception):
    """
    Ошибка при создании/измении события, когда событие с
    таким именем и датой уже существует в базе.
    """

    def __init__(self, message="Событие с таким именем и датой уже создано"):
        self.message = message
        super().__init__(message)
