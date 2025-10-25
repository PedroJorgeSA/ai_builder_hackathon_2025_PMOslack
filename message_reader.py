from datetime import datetime
from slack_utils import SlackBot

class MessageReader:
    def __init__(self):
        """Inicializa o leitor de mensagens"""
        self.slack_bot = SlackBot()
    
    def listar_mensagens_anteriores(self, canal, limite=10):
        """
        Função para ler e listar mensagens anteriores de um canal do Slack
        
        Args:
            canal (str): Nome do canal (ex: '#teste') ou ID do canal
            limite (int): Número máximo de mensagens para buscar (padrão: 10)
        
        Returns:
            list: Lista de mensagens com informações formatadas
        """
        try:
            # Se o canal começa com #, converte para ID
            canal_id = canal
            if canal.startswith('#'):
                canal_nome = canal[1:]  # Remove o #
                # Busca o ID do canal
                response_list = self.slack_bot.client.conversations_list(types="public_channel,private_channel")
                if response_list['ok']:
                    for c in response_list['channels']:
                        if c['name'] == canal_nome:
                            canal_id = c['id']
                            print(f"Usando ID do canal: {canal_id} para {canal}")
                            break
            
            # Busca o histórico de mensagens do canal
            response = self.slack_bot.client.conversations_history(channel=canal_id, limit=limite)
            
            if response['ok']:
                mensagens = response['messages']
                print(f"\n=== ÚLTIMAS {len(mensagens)} MENSAGENS DO CANAL {canal.upper()} ===\n")
                
                mensagens_formatadas = []
                
                for i, msg in enumerate(mensagens, 1):
                    # Extrai informações da mensagem
                    user_id = msg.get('user', '')
                    texto = msg.get('text', 'Sem texto')
                    timestamp = msg.get('ts', '')
                    
                    # Obtém nome real do usuário
                    if user_id:
                        nome_usuario = self.slack_bot.obter_info_usuario(user_id)
                    else:
                        nome_usuario = 'Bot ou Sistema'
                    
                    # Converte timestamp para data legível
                    if timestamp:
                        data = datetime.fromtimestamp(float(timestamp))
                        data_formatada = data.strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        data_formatada = 'Data não disponível'
                    
                    # Formata a mensagem
                    mensagem_formatada = f"{i}. [{data_formatada}] {nome_usuario}: {texto}"
                    print(mensagem_formatada)
                    mensagens_formatadas.append(mensagem_formatada)
                
                print(f"\n=== TOTAL: {len(mensagens)} mensagens encontradas ===\n")
                return mensagens_formatadas
                
            else:
                print(f"Erro ao buscar mensagens: {response['error']}")
                return []
                
        except Exception as e:
            print(f"Erro ao listar mensagens: {e}")
            return []
    
    def buscar_mensagens_por_usuario(self, canal, nome_usuario, limite=50):
        """
        Busca mensagens de um usuário específico pelo nome
        
        Args:
            canal (str): Nome do canal
            nome_usuario (str): Nome do usuário para buscar
            limite (int): Número máximo de mensagens para buscar
        
        Returns:
            list: Lista de mensagens do usuário
        """
        try:
            # Se o canal começa com #, converte para ID
            canal_id = canal
            if canal.startswith('#'):
                canal_nome = canal[1:]  # Remove o #
                # Busca o ID do canal
                response_list = self.slack_bot.client.conversations_list(types="public_channel,private_channel")
                if response_list['ok']:
                    for c in response_list['channels']:
                        if c['name'] == canal_nome:
                            canal_id = c['id']
                            break
            
            response = self.slack_bot.client.conversations_history(channel=canal_id, limit=limite)
            
            if response['ok']:
                mensagens_encontradas = []
                mensagens = response['messages']
                
                for msg in mensagens:
                    user_id = msg.get('user', '')
                    if user_id:
                        # Busca por ID do usuário ou nome
                        if nome_usuario.lower() in user_id.lower() or nome_usuario.lower() in user_id:
                            timestamp = msg.get('ts', '')
                            
                            if timestamp:
                                data = datetime.fromtimestamp(float(timestamp))
                                data_formatada = data.strftime('%d/%m/%Y %H:%M:%S')
                            else:
                                data_formatada = 'Data não disponível'
                            
                            mensagem_formatada = f"[{data_formatada}] {user_id}: {msg.get('text', '')}"
                            mensagens_encontradas.append(mensagem_formatada)
                
                print(f"\n=== {len(mensagens_encontradas)} MENSAGENS ENCONTRADAS DO USUÁRIO '{nome_usuario}' ===\n")
                for i, msg in enumerate(mensagens_encontradas, 1):
                    print(f"{i}. {msg}")
                
                return mensagens_encontradas
            else:
                print(f"Erro ao buscar mensagens: {response['error']}")
                return []
                
        except Exception as e:
            print(f"Erro ao buscar mensagens: {e}")
            return []

    def buscar_mensagens_por_texto(self, canal, texto_busca, limite=50):
        """
        Busca mensagens que contenham um texto específico
        
        Args:
            canal (str): Nome do canal
            texto_busca (str): Texto para buscar
            limite (int): Número máximo de mensagens para buscar
        
        Returns:
            list: Lista de mensagens que contêm o texto
        """
        try:
            # Se o canal começa com #, converte para ID
            canal_id = canal
            if canal.startswith('#'):
                canal_nome = canal[1:]  # Remove o #
                # Busca o ID do canal
                response_list = self.slack_bot.client.conversations_list(types="public_channel,private_channel")
                if response_list['ok']:
                    for c in response_list['channels']:
                        if c['name'] == canal_nome:
                            canal_id = c['id']
                            break
            
            response = self.slack_bot.client.conversations_history(channel=canal_id, limit=limite)
            
            if response['ok']:
                mensagens_encontradas = []
                mensagens = response['messages']
                
                for msg in mensagens:
                    texto = msg.get('text', '').lower()
                    if texto_busca.lower() in texto:
                        user_id = msg.get('user', '')
                        timestamp = msg.get('ts', '')
                        
                        if user_id:
                            nome_usuario = self.slack_bot.obter_info_usuario(user_id)
                        else:
                            nome_usuario = 'Bot ou Sistema'
                        
                        if timestamp:
                            data = datetime.fromtimestamp(float(timestamp))
                            data_formatada = data.strftime('%d/%m/%Y %H:%M:%S')
                        else:
                            data_formatada = 'Data não disponível'
                        
                        mensagem_formatada = f"[{data_formatada}] {nome_usuario}: {msg.get('text', '')}"
                        mensagens_encontradas.append(mensagem_formatada)
                
                print(f"\n=== {len(mensagens_encontradas)} MENSAGENS ENCONTRADAS COM '{texto_busca}' ===\n")
                for i, msg in enumerate(mensagens_encontradas, 1):
                    print(f"{i}. {msg}")
                
                return mensagens_encontradas
            else:
                print(f"Erro ao buscar mensagens: {response['error']}")
                return []
                
        except Exception as e:
            print(f"Erro ao buscar mensagens: {e}")
            return []
    
    def testar_canais_disponiveis(self, canais_para_testar):
        """
        Testa uma lista de canais para ver quais têm mensagens
        
        Args:
            canais_para_testar (list): Lista de canais para testar
        
        Returns:
            dict: Dicionário com canais que funcionaram e suas mensagens
        """
        resultados = {}
        
        for canal in canais_para_testar:
            print(f"\nTestando canal #{canal}...")
            mensagens = self.listar_mensagens_anteriores(f"#{canal}", limite=5)
            if mensagens:
                resultados[f"#{canal}"] = mensagens
                print(f"Canal #{canal} tem {len(mensagens)} mensagens!")
            else:
                print(f"Canal #{canal} não encontrado ou sem mensagens.")
        
        return resultados
