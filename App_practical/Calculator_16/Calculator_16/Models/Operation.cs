using System.ComponentModel.DataAnnotations;

namespace Calculator_16.Models
{
    public enum Operation
    {
        [Display(Name = "Сложение")]
        Add = 1,
        [Display(Name = "Вычитание")]
        Subtract = 2,
        [Display(Name = "Умножение")]
        Multiply = 3,
        [Display(Name = "Деление")]
        Divide = 4
    }
}