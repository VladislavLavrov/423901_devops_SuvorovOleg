# optimizer/admin.py
from django.contrib import admin
from .models import FurnaceCalculation

@admin.register(FurnaceCalculation)
class FurnaceCalculationAdmin(admin.ModelAdmin):
    list_display = ('id', 'optimal_power', 'optimal_velocity', 
                    'calculated_max_temperature', 'success', 'created_at')
    list_filter = ('success', 'created_at')
    search_fields = ('id', 'error_message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Параметры ввода', {
            'fields': (
                ('power_min', 'power_max'),
                ('velocity_min', 'velocity_max'),
                ('time_min', 'time_max'),
                ('thickness_min', 'thickness_max'),
            )
        }),
        ('Результаты', {
            'fields': (
                ('optimal_power', 'optimal_velocity'),
                ('optimal_time', 'optimal_thickness'),
                ('calculated_max_temperature', 'calculated_heating_rate'),
                ('min_objective_value', 'balance_error'),
            )
        }),
        ('Статус', {
            'fields': ('success', 'error_message', 'created_at')
        }),
    )