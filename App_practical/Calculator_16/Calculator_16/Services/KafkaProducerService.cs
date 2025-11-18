using Calculator_16.Services;
using Confluent.Kafka;
using System;
using System.Threading.Tasks;

namespace Calculator_16.Services
{
    public class KafkaProducerService<K, V>
    {
        private readonly IProducer<K, V> _kafkaHandle;

        public KafkaProducerService(KafkaProducerHandler handle)
        {
            _kafkaHandle = new DependentProducerBuilder<K, V>(handle.Handle).Build();
        }

        /// <summary>
        /// Asynchronously produce a message and expose delivery information
        /// via the returned Task. Use this method of producing if you would
        /// like to await the result before flow of execution continues.
        /// </summary>
        public Task ProduceAsync(string topic, Message<K, V> message)
            => _kafkaHandle.ProduceAsync(topic, message);

        /// <summary>
        /// Asynchronously produce a message and expose delivery information
        /// via the provided callback function. Use this method of producing
        /// if you would like flow of execution to continue immediately, and
        /// handle delivery information out-of-band.
        /// </summary>
        public void Produce(string topic, Message<K, V> message, Action<DeliveryReport<K, V>> deliveryHandler = null)
            => _kafkaHandle.Produce(topic, message, deliveryHandler);

        public void Flush(TimeSpan timeout)
            => _kafkaHandle.Flush(timeout);
    }
}