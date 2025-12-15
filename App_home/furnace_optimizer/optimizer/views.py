from django.shortcuts import render, redirect
from .optimization import optimize_parameters
from django.http import HttpResponse

def index_view(request):
    """Главная страница с формой ввода"""
    return render(request, 'optimizer/index.html')

def calculate_view(request):
    """Обработка расчета и вывод результатов"""
    if request.method == 'POST':
        # Получаем данные из формы
        params = {
            'P_min': float(request.POST.get('P_min', 1000)),
            'P_max': float(request.POST.get('P_max', 5000)),
            'v_min': float(request.POST.get('v_min', 0.5)),
            'v_max': float(request.POST.get('v_max', 2.0)),
            't_min': float(request.POST.get('t_min', 60)),
            't_max': float(request.POST.get('t_max', 3600)),
            'd_min': float(request.POST.get('d_min', 0.05)),
            'd_max': float(request.POST.get('d_max', 0.3)),
            'w1': float(request.POST.get('w1', 0.7)),
            'w2': float(request.POST.get('w2', 0.3)),
            'alpha1': float(request.POST.get('alpha1', 0.00002)),
            'alpha2': float(request.POST.get('alpha2', 0.0001)),
            'R_max': float(request.POST.get('R_max', 10)),
            'C': float(request.POST.get('C', 460)),
            'm': float(request.POST.get('m', 5)),
            'T_init': float(request.POST.get('T_init', 20)),
            'T_target': float(request.POST.get('T_target', 800)),
            'T_max': float(request.POST.get('T_max', 820)),
            'η0': float(request.POST.get('η0', 0.8)),
            'kv': float(request.POST.get('kv', 0.1)),
            'β': float(request.POST.get('β', 5)),
            'vo': float(request.POST.get('vo', 1)),
            'kd': float(request.POST.get('kd', 0.05)),
            'do': float(request.POST.get('do', 0.15)),
        }
        # Запускаем оптимизацию
        results = optimize_parameters(params)
        # Сохраняем параметры и результаты в сессии для графиков
        request.session['params'] = params
        request.session['results'] = results
        # Форматируем результаты для отображения
        formatted_results = {
            'optimal_P': f"{results['optimal_P']:.2f}",
            'optimal_v': f"{results['optimal_v']:.2f}",
            'optimal_t': f"{results['optimal_t']:.2f}",
            'optimal_d': f"{results['optimal_d']:.2f}",
            'min_value': f"{results['min_value']:.2f}",
            'max_temperature': f"{results['max_temperature']:.2f}",
            'heating_rate': f"{results['heating_rate']:.2f}",
            'balance_error': f"{results['balance_error']:.2f}"
        }
        return render(request, 'optimizer/results.html', {
            'params': params,
            'results': formatted_results
        })
    # Если не POST, вернем на главную
    return render(request, 'optimizer/index.html')