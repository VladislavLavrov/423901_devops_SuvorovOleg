import numpy as np
from scipy.optimize import minimize


# === 2. Функции модели ===
def eta(v: float, d: float, η0, kv, β, vo, kd, do) -> float:
    """КПД печи"""
    return η0 + kv *np.tanh(β * (v - vo)) - kd * (d - do)
    #return 0.8 + 0.1*np.tanh(5*(v-1)) - 0.05*(d-0.15)

def calculate_max_temperature(x, T_init: int, C: int, m: float, η0, kv, β, vo, kd, do) -> int:
    """Расчет максимальной температуры в заготовке"""
    P, v, t, d = x
    # Ваш расчет температуры (замените на реальную модель)
    return T_init + P * t * eta(v, d, η0, kv, β, vo, kd, do) / (C * m) 

def calculate_heating_rate(x, alpha1, alpha2):
    """Расчет темпа нагрева"""
    P, v, t, d = x
    # Ваш расчет темпа нагрева
    return alpha1 * P / d**2 - alpha2 * v

def thermal_balance_error(x, C, m, T_target, T_init, η0, kv, β, vo, kd, do):
    """Ошибка теплового баланса (должна стремиться к 0)"""
    P, v, t, d = x
    return C * m * (T_target - T_init) - P * t * eta(v, d, η0, kv, β, vo, kd, do)

    # Целевая функция для минимизации
def objective(x, w1, w2):
    P, v, t, d = x
    # Простая модель для демонстрации (замените на вашу реальную модель)
    uniformity = 50.0 / (P * t / 1e6)  # "Равномерность" нагрева
    energy = P * t / 1e6                # Энергозатраты
    return w1 * uniformity + w2 * energy

def optimize_parameters(params):
    """Оптимизация параметров нагрева"""
    P_min, P_max = params['P_min'], params['P_max']
    v_min, v_max = params['v_min'], params['v_max']
    t_min, t_max = params['t_min'], params['t_max']
    d_min, d_max = params['d_min'], params['d_max']
    w1, w2 = params['w1'], params['w2']
    alpha1, alpha2 = params['alpha1'], params['alpha2']
    R_max = params['R_max']
    C, m = params['C'], params['m']
    T_init, T_target, T_max = params['T_init'], params['T_target'], params['T_max']
    η0, kv, β, vo, kd, do = params['η0'], params['kv'], params['β'], params['vo'], params['kd'], params['do']

    P0 = float((P_min + P_max) / 2)
    v0 = float((v_min + v_max) / 2)
    d0 = float((d_min + d_max) / 2)
    t0 = float(C * m * (T_target - T_init) / (P0 * eta(v0, d0, η0, kv, β, vo, kd, do)))

    # Начальное приближение
    x0 = [
        P0,
        v0,
        d0,
        t0
    ]
    
    # Границы параметров
    bounds = [
        (P_min, P_max),
        (v_min, v_max),
        (t_min, t_max),
        (d_min, d_max)
    ]

    # Параметры оптимизации
    options = {
        'maxiter': 1000,
        'ftol': 1e-6,
        'disp': True
    }

    # Определение ограничений
    constraints = [
        # Ограничение на максимальную температуру
        {'type': 'ineq', 'fun': lambda x: T_max - calculate_max_temperature(x, T_init, C, m, η0, kv, β, vo, kd, do)},
        
        # Ограничение на темп нагрева
        {'type': 'ineq', 'fun': lambda x: R_max - calculate_heating_rate(x, alpha1, alpha2)},
        
        # Ограничение на тепловой баланс (должен быть равен 0)
        {'type': 'eq', 'fun': lambda x: thermal_balance_error(x, C, m, T_target, T_init, η0, kv, β, vo, kd, do)}
    ]
    
# Запуск оптимизации с ограничениями
    res = minimize(
        objective,
        x0,
        method='SLSQP',
        args=(w1, w2),
        bounds=bounds,
        constraints=constraints,
        options=options
    )

    if not res.success:
        raise ValueError(f"Оптимизация не удалась: {res.message}")
    
    return {
        'optimal_P': res.x[0],
        'optimal_v': res.x[1],
        'optimal_t': res.x[2],
        'optimal_d': res.x[3],
        'min_value': res.fun,
        'max_temperature': round(calculate_max_temperature(res.x, T_init, C, m, η0, kv, β, vo, kd, do), 2),
        'heating_rate': round(calculate_heating_rate(res.x, alpha1, alpha2), 2),
        'balance_error': round(thermal_balance_error(res.x, C, m, T_target, T_init, η0, kv, β, vo, kd, do), 5)
    }
    