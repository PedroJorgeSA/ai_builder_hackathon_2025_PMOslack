import slack  # importa a biblioteca do Slack
import os     # importa a biblioteca para manipular variáveis de ambiente e sistema
from pathlib import Path  # importa Path para trabalhar com caminhos de arquivos
from dotenv import load_dotenv  # importa a função para carregar variáveis de ambiente de um arquivo .env

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

try:
    client.chat_postMessage(channel='#teste', text="Hello World")
    print("Message sent to #general channel successfully!")
except Exception as e:
    print(f"Failed to send to #general: {e}")
    try:
        client.chat_postMessage(channel='#test', text="Hello World")
        print("Message sent to #test channel successfully!")
    except Exception as e2:
        print(f"Failed to send to #test: {e2}")
        print("Please create a #test channel in your Slack workspace or use an existing channel.")
