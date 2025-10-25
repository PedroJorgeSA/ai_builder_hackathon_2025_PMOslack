# Teste específico para investigar o nome do usuário
from slack_utils import SlackBot
from message_reader import MessageReader

def teste_usuario():
    print("=== TESTE: INVESTIGANDO NOME DO USUÁRIO ===")
    
    bot = SlackBot()
    reader = MessageReader()
    
    # 1. Lista mensagens e mostra IDs dos usuários
    print("\n1. Listando mensagens com IDs dos usuários...")
    mensagens = reader.listar_mensagens_anteriores('#teste', limite=10)
    
    # 2. Testa obter nome do usuário U09P08RF11P (que aparece nas mensagens)
    print("\n2. Testando obter nome do usuário U09P08RF11P...")
    nome_usuario = bot.obter_info_usuario('U09P08RF11P')
    print(f"Nome do usuário U09P08RF11P: {nome_usuario}")
    
    # 3. Testa obter nome do usuário U09NHUGED5K (bot)
    print("\n3. Testando obter nome do usuário U09NHUGED5K...")
    nome_bot = bot.obter_info_usuario('U09NHUGED5K')
    print(f"Nome do usuário U09NHUGED5K: {nome_bot}")
    
    # 4. Busca por diferentes variações do nome
    print("\n4. Testando busca por diferentes variações...")
    variacoes = ['pedro', 'soares', 'pedro.soares', 'Pedro', 'Soares']
    
    for variacao in variacoes:
        print(f"\nBuscando por '{variacao}':")
        mensagens = reader.buscar_mensagens_por_usuario('#teste', variacao, limite=10)

if __name__ == "__main__":
    teste_usuario()
