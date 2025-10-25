# Debug para investigar por que não está lendo as mensagens mais recentes
from slack_utils import SlackBot
from message_reader import MessageReader

def debug_mensagens():
    print("=== DEBUG: INVESTIGANDO MENSAGENS RECENTES ===")
    
    bot = SlackBot()
    reader = MessageReader()
    
    # 1. Testa com limite maior
    print("\n1. Testando com limite maior (20 mensagens)...")
    mensagens = reader.listar_mensagens_anteriores('#teste', limite=20)
    
    # 2. Busca especificamente por "pedro.soares"
    print("\n2. Buscando especificamente por 'pedro.soares'...")
    mensagens_pedro = reader.buscar_mensagens_por_texto('#teste', 'pedro.soares', limite=50)
    
    # 3. Busca por "teste" (que aparece nas mensagens)
    print("\n3. Buscando por 'teste'...")
    mensagens_teste = reader.buscar_mensagens_por_texto('#teste', 'teste', limite=50)
    
    # 4. Busca por "@PMO bot" (que aparece nas mensagens)
    print("\n4. Buscando por '@PMO bot'...")
    mensagens_pmo = reader.buscar_mensagens_por_texto('#teste', '@PMO bot', limite=50)
    
    # 5. Lista todas as mensagens sem filtro
    print("\n5. Listando TODAS as mensagens (limite 50)...")
    todas_mensagens = reader.listar_mensagens_anteriores('#teste', limite=50)

if __name__ == "__main__":
    debug_mensagens()
