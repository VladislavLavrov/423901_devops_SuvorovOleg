using Microsoft.AspNetCore.Mvc;

namespace CalculatorApp.Controllers
{
    public enum Operation
    {
        Add, Subtract, Multiply, Divide
    }
    public class CalculatorController : Controller
    {
        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Calculate(double num1, double num2, Operation operation)
        {
            double result = 0;

            switch (operation)
            {
                case Operation.Add:
                    result = num1 + num2;
                    break;
                case Operation.Subtract:
                    result = num1 - num2;
                    break;
                case Operation.Multiply:
                    result = num1 * num2;
                    break;
                case Operation.Divide:
                    if (num2 == 0)
                    {
                        ViewBag.Error = "Ошибка: деление на ноль!";
                        return View("Index");
                    }
                    result = num1 / num2;
                    break;
            }

            ViewBag.Result = result;    
            ViewBag.Num1 = num1; // Сохраняем значения для формы
            ViewBag.Num2 = num2; // Сохраняем значения для формы
            ViewBag.Operation = operation;
            return View("Index");
        }
    }
}