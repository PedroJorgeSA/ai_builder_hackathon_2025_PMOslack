import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

class SlackBot:
    def __init__(self):
        """Inicializa o bot do Slack com as configurações necessárias"""
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    
    def enviar_mensagem(self, canal, texto):
        """
        Envia uma mensagem para um canal do Slack
        
        Args:
            canal (str): Nome do canal (ex: '#teste')
            texto (str): Texto da mensagem
        
        Returns:
            bool: True se enviou com sucesso, False caso contrário
        """
        try:
            response = self.client.chat_postMessage(channel=canal, text=texto)
            if response['ok']:
                print(f"Mensagem enviada para {canal}: {texto}")
                return True
            else:
                print(f"Erro ao enviar mensagem: {response['error']}")
                return False
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False
    
    def obter_info_usuario(self, user_id):
        """
        Obtém informações do usuário pelo ID
        
        Args:
            user_id (str): ID do usuário no Slack
        
        Returns:
            str: Nome do usuário ou ID se não conseguir obter
        """
        try:
            response = self.client.users_info(user=user_id)
            if response['ok']:
                user_info = response['user']
                return user_info.get('real_name', user_info.get('name', user_id))
            else:
                return user_id
        except:
            return user_id
    
    def adicionar_bot_ao_canal(self, canal):
        """
        Adiciona o bot a um canal específico
        
        Args:
            canal (str): Nome do canal (ex: 'teste')
        
        Returns:
            bool: True se adicionou com sucesso, False caso contrário
        """
        try:
            # Primeiro, busca o ID do canal
            response = self.client.conversations_list(types="public_channel,private_channel")
            if not response['ok']:
                print(f"Erro ao listar canais: {response['error']}")
                return False
            
            canal_id = None
            canal_nome = canal.replace('#', '')
            
            print(f"Procurando canal '{canal_nome}'...")
            for c in response['channels']:
                print(f"  Canal encontrado: {c['name']} (ID: {c['id']})")
                if c['name'] == canal_nome:
                    canal_id = c['id']
                    print(f"  Canal '{canal_nome}' encontrado! ID: {canal_id}")
                    break
            
            if not canal_id:
                print(f"Canal '{canal_nome}' não encontrado na lista de canais")
                return False
            
            # Tenta adicionar o bot ao canal
            print(f"Tentando adicionar bot ao canal {canal_nome} (ID: {canal_id})...")
            join_response = self.client.conversations_join(channel=canal_id)
            if join_response['ok']:
                print(f"Bot adicionado ao canal {canal_nome} com sucesso!")
                return True
            else:
                print(f"Erro ao adicionar bot ao canal {canal_nome}: {join_response['error']}")
                return False
                
        except Exception as e:
            print(f"Erro ao adicionar bot ao canal: {e}")
            return False
    
    def listar_canais_disponiveis(self):
        """
        Lista todos os canais disponíveis no workspace
        
        Returns:
            list: Lista de canais disponíveis
        """
        try:
            response = self.client.conversations_list(types="public_channel,private_channel")
            if response['ok']:
                canais = []
                for canal in response['channels']:
                    canais.append({
                        'nome': canal['name'],
                        'id': canal['id'],
                        'membros': canal.get('num_members', 0)
                    })
                return canais
            else:
                print(f"Erro ao listar canais: {response['error']}")
                return []
        except Exception as e:
            print(f"Erro ao listar canais: {e}")
            return []
