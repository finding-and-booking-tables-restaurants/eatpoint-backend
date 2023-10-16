# Максимальное количество мест
MAX_SEATS = 100

# Минимальное количество мест
MIN_SEATS = 0

# Максимальный размер изображения
IMAGE_SIZE = 5 * 1024 * 1024

# Интервал времени
INTERVAL_MINUTES = 30


START_TIME = "08:00"


END_TIME = "18:00"

# Размер страницы
PAGE_SIZE = 10

# Дни недели
DAYS = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
]

# Средний чек
CHECKS = ["до 1000", "1000 - 2000", "2000 - 3000", "от 3000"]

# Роли
CLIENT = "client"
RESTORATEUR = "restorateur"
MODERATOR = "moderator"
ADMIN = "admin"
SUPERUSER = "superuser"

# Диапазон кода подтверждения
MIN_LIMIT_CONFIRM_CODE = 100_000
MAX_LIMIT_CONFIRM_CODE = 999_999

# Способы отправки кода подтверждения
SMS = "sms"
EMAIL = "email"
TELEGRAM = "telegram"
NOTHING = "nothing"
