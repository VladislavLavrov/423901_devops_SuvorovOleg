using Calculator_16.Data;
using Microsoft.EntityFrameworkCore;

namespace Calculator_16.Data
{
    public class CalculatorContext : DbContext
    {
        public DbSet<DataInputVariant> DataInputVariants
        { get; set; }
        public CalculatorContext(DbContextOptions<CalculatorContext> options) : base(options)
        {
        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            //OnModelCreating(modelBuilder);
        }
    }
}