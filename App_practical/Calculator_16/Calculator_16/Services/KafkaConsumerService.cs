using Calculator_16.Data;
using Calculator_16.Models;
using Confluent.Kafka;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using System;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;


namespace Calculator_16.Services
{
    using Calculator_16.Data;
    using Confluent.Kafka;
    using Microsoft.Extensions.Configuration;
    using Microsoft.Extensions.DependencyInjection;
    using Microsoft.Extensions.Hosting;
    using System;
    using System.Net.Http;
    using System.Text.Json;
    using System.Threading;
    using System.Threading.Tasks;

    public class KafkaConsumerService : BackgroundService
    {
        private readonly string _topic;
        private readonly IConsumer<Null, string> _kafkaConsumer;
        private readonly IServiceProvider _serviceProvider;
        private readonly IHttpClientFactory _clientFactory;

        public KafkaConsumerService(IConfiguration config, IServiceProvider serviceProvider, IHttpClientFactory clientFactory)
        {
            // Конфигурирование настроек Kafka и инициализация компонентов
            var consumerConfig = new ConsumerConfig();
            config.GetSection("Kafka:ConsumerSettings").Bind(consumerConfig);
            _topic = config.GetValue<string>("Kafka:TopicName");
            _kafkaConsumer = new ConsumerBuilder<Null, string>(consumerConfig).Build();
            _serviceProvider = serviceProvider;
            _clientFactory = clientFactory;
        }

        /// <summary>
        /// Выполнение работы Kafka Consumer'а.
        /// </summary>
        protected override Task ExecuteAsync(CancellationToken stoppingToken)
        {
            return Task.Run(() => StartConsumerLoop(stoppingToken), stoppingToken);
        }

        /// <summary>
        /// Цикл обработки сообщений из Kafka.
        /// </summary>
        /// <param name="cancellationToken">Токен отмены операции.</param>
        private async Task StartConsumerLoop(CancellationToken cancellationToken)
        {
            _kafkaConsumer.Subscribe(_topic);

            while (!cancellationToken.IsCancellationRequested)
            {
                try
                {
                    var cr = _kafkaConsumer.Consume(cancellationToken);

                    // Десериализация исходных данных
                    var inputData = JsonSerializer.Deserialize<DataInputVariant>(cr.Message.Value);

                    // Выполнение расчета
                    var result = CalculatorLibrary.CalculateOperation(
                        inputData.Operand_1,
                        inputData.Operand_2,
                        inputData.Type_operation);

                    inputData.Result = result.ToString();
                    var httpClient = _clientFactory.CreateClient();

                    // Заменить последние 2 цифры порта на порядковый номер из студенческого журнала
                    // Например, порт 5012 соответствует номеру 12
                    await httpClient.PostAsJsonAsync($"http://localhost:5016/Calculator/Callback", inputData);

                    // Обработка сообщения...
                    Console.WriteLine($"Message key: {cr.Message.Key}, value: {cr.Message.Value}");
                }
                catch (OperationCanceledException)
                {
                    break;
                }
                catch (ConsumeException e)
                {
                    if (e.Error.IsFatal)
                    {
                        // https://github.com/edenhill/librdkafka/blob/master/INTRODUCTION.md#fatal-consumer-errors
                        break;
                    }
                }
                catch (Exception e)
                {
                    break;
                }
            }
        }

        /// <summary>
        /// Очистка ресурсов Consumer'а при завершении работы сервиса.
        /// </summary>
        public override void Dispose()
        {
            _kafkaConsumer.Close(); // Фиксация оффсетов и корректное выход из группы
            _kafkaConsumer.Dispose();
            base.Dispose();
        }
    }
}