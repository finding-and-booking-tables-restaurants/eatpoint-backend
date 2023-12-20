# Время жизни JWT токенов
ACCESS_TOKEN_LIFETIME_MINUTES = 1440
REFRESH_TOKEN_LIFETIME_DAYS = 30

# Максимальное количество мест
MAX_SEATS = 100

# Минимальное количество мест
MIN_SEATS = 0

# Максимальный размер изображения
IMAGE_SIZE = 1 * 1024 * 1024

IMAGE_COUNT = 10

# Интервал времени
INTERVAL_MINUTES = 30

# Начальное время(для генератора времени работы)
START_TIME = "00:00"

# Конечное время(для генератора времени работы)
END_TIME = "23:30"

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

# Количество дней для формирования слотов
AVAILABLE_DAYS = 30

# Средний чек
CHECKS = ["до 1000", "1000 - 2000", "2000 - 3000", "от 3000"]

# Роли
CLIENT = "client"
RESTORATEUR = "restorateur"
ADMINISTRATOR = "admin_restorana"
MODERATOR = "moderator"
ADMIN = "admin"
SUPERUSER = "superuser"

# Диапазон кода подтверждения
MIN_LIMIT_CONFIRM_CODE = 100_000
MAX_LIMIT_CONFIRM_CODE = 999_999

# Диапазон кода подтверждения бронирования
MIN_LIMIT_RESERVATION_CODE = 1000
MAX_LIMIT_RESERVATION_CODE = 9999

# Способы отправки кода подтверждения
SMS = "sms"
EMAIL = "email"
TELEGRAM = "telegram"
NOTHING = "nothing"
