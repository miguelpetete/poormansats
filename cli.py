import click, pika, json, os, requests
from dotenv import dotenv_values

envs = dotenv_values(".env")
key = envs['AIRTABLE_KEY']
baseID = envs['AIRTABLE_BASE_ID']
tableID = envs['AIRTABLE_TABLE_ID']

basic_url = 'https://api.airtable.com/v0/'

def upload_airtable(obj):
    url = basic_url + str(baseID) + '/' + str(tableID)
    headers = {
        "Authorization": f"Bearer {str(key)}", 
        "Content-type": "application/json"
    }
    response = requests.post(url, headers=headers, json=obj)
    print('Updated!!')

def on_message_received(ch,method,properties,body):
    message = json.loads(body)
    fullname = message['name'] + ' ' + message['first_surname'] + ' ' + message['second_surname']
    airtable_object = {
        "records": [
            {
                "fields": {
                    "Status": "Inbox",
                    "Email": f"{message['email']}",
                    "Name": f"{fullname}",
                }
            }
        ]
    }
    print('Updating candidate to AirTable')
    upload_airtable(airtable_object)
    print('Done. Please, press Control+C')

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