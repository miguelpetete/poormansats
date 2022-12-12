import click, pika

def on_message_received(ch,method,properties,body):
    print(f"Received message: {body}")

def consuming():
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='letterbox')
    channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_message_received)
    print("Starting consuming")
    channel.start_consuming()

@click.command()
@click.option('--consume', default=0, help='Number of greetings.')
def cli(consume):
    if consume == 1:
        consuming()

if __name__ == '__main__':
    cli()