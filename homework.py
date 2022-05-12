from typing import Dict, Type, ClassVar, List, Tuple
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить сообщение заданного формата с данными по тренировке."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Для треннировки {self.__class__.__name__}'
                                  f' не определен метод расчета каллорий')

    def get_duration_in_min(self) -> float:
        """Получить время затраченное на тренировку в минутах."""
        return self.duration * self.MIN_IN_HOUR

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_1: ClassVar[int] = 18
    COEFF_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_1 * self.get_mean_speed() - self.COEFF_2)
                * self.weight / self.M_IN_KM * self.get_duration_in_min())


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    COEFF_1: ClassVar[float] = 0.035
    COEFF_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_1 * self.weight + (self.get_mean_speed() ** 2
                 // self.height) * self.COEFF_2
                 * self.weight) * self.get_duration_in_min())


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_1: ClassVar[float] = 1.1
    COEFF_2: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_1) * self.COEFF_2
                * self.weight)


def read_package(workout_type: str, data: Tuple[str, List[float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                    'RUN': Running,
                                                    'WLK': SportsWalking}
        return training_type[workout_type](*data)
    except TypeError:
        print('Неверный тип тренировки.')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        info = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        print('Недостаточно данных для получения информации.')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
