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
                    "Notified": False
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

def update_notify(record):
    url = basic_url + str(baseID) + '/' + str(tableID)
    headers = {
        "Authorization": f"Bearer {str(key)}", 
        "Content-type": "application/json"
    }
    airtable_object = {
        "records": [
            {
                "fields": {
                    "Status": record["fields"]["Status"],
                    "Email": record["fields"]["Email"],
                    "Name": record["fields"]["Name"],
                    "Notified": True
                }
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=airtable_object)


def send_message():
    url = basic_url + str(baseID) + '/' + str(tableID)
    headers = {
        "Authorization": f"Bearer {str(key)}"
    }
    response = requests.get(url, headers=headers)
    res = response.json()
    for record in res["records"]:
        status = record["fields"]["Status"]
        if status == "Rejected":
            name = record["fields"]["Name"]
            print(f"Candidate: {name} is REJECTED")
            update_notify(record)
        elif status == "Hired":
            name = record["fields"]["Name"]
            print(f"Candidate: {name} is HIRED")
            update_notify(record)


@click.command()
@click.option('--consume', default=0, help='If it is 1, it consume from rabbit to publish in Airtable.')
@click.option('--candidates', default=0, help='If candidates are Rejected or Hired, they send an email to them with the result. If it is 1, it sends the emails.')
def cli(consume,candidates):
    if consume == 1:
        consuming()
    elif candidates == 1:
        send_message()

if __name__ == '__main__':
    cli()