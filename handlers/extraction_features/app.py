import json as j
from config import Config
from event_handler import EventHandler
from azure.servicebus import ServiceBusClient, ServiceBusReceiveMode


if __name__ == '__main__':
    config = Config()
    with ServiceBusClient.from_connection_string(config.AZURE_SERVICE_BUS_CONNECTION_STRING) as client:
        with client.get_queue_receiver(config.AZURE_SERVICE_BUS_QUEUE_NAME, max_wait_time=None, receive_mode=ServiceBusReceiveMode.PEEK_LOCK) as receiver:
            for msg in receiver:  # ServiceBusReceiver instance is a generator.
                payloads = [j.loads(payload) for payload in msg.body]
                event_handler = EventHandler(config)
                
                result = event_handler.handler_event(payloads[0])

                if result:
                    receiver.complete_message(msg)
                else:
                    receiver.dead_letter_message(msg, reason='Não foi possível obter os dados da analise')

