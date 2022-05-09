M_IN_KM = 1000
MIN_IN_HOUR = 60


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type  # имя класса тренировки
        self.duration = duration  # длительность тренировки в часах
        self.distance = distance  # дистанция в километрах
        self.speed = speed  # средняя скорость
        self.calories = calories  # количество израсходованных килокалорий

    def get_message(self) -> str:
        """Вернуть строку сообщений."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {round(self.duration, 3)} ч.; '
                f'Дистанция: {round(self.distance, 3)} км; '
                f'Ср. скорость: {round(self.speed, 3)} км/ч; '
                f'Потрачено ккал: {round(self.calories, 3)}.'
                )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # количество совершённых действий
        self.duration = duration  # длительность тренировки
        self.weight = weight  # вес спортсмена
        self.dur_min = self.duration * MIN_IN_HOUR

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 18
        coeff_calorie_2 = 20

        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) *
                self.weight / M_IN_KM * self.duration * self.dur_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # рост спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029

        return ((coeff_calorie_1 * self.height + (self.get_mean_speed() ** 2 //
                self.height) * coeff_calorie_2 * self.height) * self.dur_min)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # сколько раз переплыл бассейн

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool / M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2

        return ((self.get_mean_speed() + coeff_calorie_1) * coeff_calorie_2 *
                self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
