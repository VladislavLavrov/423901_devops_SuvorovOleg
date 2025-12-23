# optimizer/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FurnaceCalculation(models.Model):
    """Модель для сохранения результатов расчета печи"""
    id = models.AutoField(primary_key=True, verbose_name='ID')
    
    # === Параметры ввода ===
    
    # Мощность (P)
    power_min = models.FloatField(
        verbose_name='Минимальная мощность (P_min)',
        validators=[MinValueValidator(0)]
    )
    power_max = models.FloatField(
        verbose_name='Максимальная мощность (P_max)',
        validators=[MinValueValidator(0)]
    )
    
    # Скорость (v)
    velocity_min = models.FloatField(
        verbose_name='Минимальная скорость (v_min)',
        validators=[MinValueValidator(0)]
    )
    velocity_max = models.FloatField(
        verbose_name='Максимальная скорость (v_max)',
        validators=[MinValueValidator(0)]
    )
    
    # Время (t)
    time_min = models.FloatField(
        verbose_name='Минимальное время (t_min)',
        validators=[MinValueValidator(0)]
    )
    time_max = models.FloatField(
        verbose_name='Максимальное время (t_max)',
        validators=[MinValueValidator(0)]
    )
    
    # Толщина (d)
    thickness_min = models.FloatField(
        verbose_name='Минимальная толщина (d_min)',
        validators=[MinValueValidator(0.01)]
    )
    thickness_max = models.FloatField(
        verbose_name='Максимальная толщина (d_max)',
        validators=[MinValueValidator(0.01)]
    )
    
    # Веса
    weight_uniformity = models.FloatField(
        verbose_name='Вес равномерности (w1)',
        default=0.7,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    weight_energy = models.FloatField(
        verbose_name='Вес энергии (w2)',
        default=0.3,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    
    # Коэффициенты
    alpha1 = models.FloatField(
        verbose_name='Коэффициент alpha1',
        default=0.00002
    )
    alpha2 = models.FloatField(
        verbose_name='Коэффициент alpha2',
        default=0.0001
    )
    
    # Ограничения
    max_heating_rate = models.FloatField(
        verbose_name='Максимальный темп нагрева (R_max)',
        default=10.0
    )
    
    # Теплофизические свойства
    heat_capacity = models.FloatField(
        verbose_name='Теплоемкость (C)',
        default=460.0
    )
    mass = models.FloatField(
        verbose_name='Масса (m)',
        default=5.0
    )
    
    # Температуры
    initial_temperature = models.FloatField(
        verbose_name='Начальная температура (T_init)',
        default=20.0
    )
    target_temperature = models.FloatField(
        verbose_name='Целевая температура (T_target)',
        default=800.0
    )
    max_temperature_limit = models.FloatField(
        verbose_name='Максимальная температура (T_max)',
        default=820.0
    )
    
    # Параметры КПД
    eta0 = models.FloatField(
        verbose_name='Базовый КПД (η0)',
        default=0.8
    )
    kv = models.FloatField(
        verbose_name='Коэффициент kv',
        default=0.1
    )
    beta = models.FloatField(
        verbose_name='Коэффициент β',
        default=5.0
    )
    v0 = models.FloatField(
        verbose_name='Опорная скорость (v0)',
        default=1.0
    )
    kd = models.FloatField(
        verbose_name='Коэффициент kd',
        default=0.05
    )
    d0 = models.FloatField(
        verbose_name='Опорная толщина (d0)',
        default=0.15
    )
    
    # === Результаты оптимизации ===
    
    optimal_power = models.FloatField(
        verbose_name='Оптимальная мощность (P)',
        null=True, blank=True
    )
    optimal_velocity = models.FloatField(
        verbose_name='Оптимальная скорость (v)',
        null=True, blank=True
    )
    optimal_time = models.FloatField(
        verbose_name='Оптимальное время (t)',
        null=True, blank=True
    )
    optimal_thickness = models.FloatField(
        verbose_name='Оптимальная толщина (d)',
        null=True, blank=True
    )
    
    min_objective_value = models.FloatField(
        verbose_name='Минимальное значение целевой функции',
        null=True, blank=True
    )
    calculated_max_temperature = models.FloatField(
        verbose_name='Рассчитанная максимальная температура',
        null=True, blank=True
    )
    calculated_heating_rate = models.FloatField(
        verbose_name='Рассчитанный темп нагрева',
        null=True, blank=True
    )
    balance_error = models.FloatField(
        verbose_name='Ошибка теплового баланса',
        null=True, blank=True
    )
    
    # === Метаданные ===
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    success = models.BooleanField(
        verbose_name='Успешность расчета',
        default=True
    )
    error_message = models.TextField(
        verbose_name='Сообщение об ошибке',
        blank=True, null=True
    )
    
    class Meta:
        verbose_name = 'Расчет печи'
        verbose_name_plural = 'Расчеты печи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['success']),
        ]
    
    def __str__(self):
        if self.optimal_power and self.optimal_velocity:
            return f'Расчет {self.id}: P={self.optimal_power:.1f}, v={self.optimal_velocity:.2f}'
        return f'Расчет {self.id} ({self.created_at})'
    
    def get_parameters_dict(self):
        """Возвращает параметры в формате для функции optimize_parameters"""
        return {
            'P_min': self.power_min,
            'P_max': self.power_max,
            'v_min': self.velocity_min,
            'v_max': self.velocity_max,
            't_min': self.time_min,
            't_max': self.time_max,
            'd_min': self.thickness_min,
            'd_max': self.thickness_max,
            'w1': self.weight_uniformity,
            'w2': self.weight_energy,
            'alpha1': self.alpha1,
            'alpha2': self.alpha2,
            'R_max': self.max_heating_rate,
            'C': self.heat_capacity,
            'm': self.mass,
            'T_init': self.initial_temperature,
            'T_target': self.target_temperature,
            'T_max': self.max_temperature_limit,
            'η0': self.eta0,
            'kv': self.kv,
            'β': self.beta,
            'vo': self.v0,
            'kd': self.kd,
            'do': self.d0,
        }
    
    def save_results(self, results_dict):
        """Сохраняет результаты оптимизации"""
        self.optimal_power = results_dict.get('optimal_P')
        self.optimal_velocity = results_dict.get('optimal_v')
        self.optimal_time = results_dict.get('optimal_t')
        self.optimal_thickness = results_dict.get('optimal_d')
        self.min_objective_value = results_dict.get('min_value')
        self.calculated_max_temperature = results_dict.get('max_temperature')
        self.calculated_heating_rate = results_dict.get('heating_rate')
        self.balance_error = results_dict.get('balance_error')
        self.success = True
        self.save()
    
    def mark_as_failed(self, error_message):
        """Отмечает расчет как неудачный"""
        self.success = False
        self.error_message = error_message
        self.save()