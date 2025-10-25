# Importa os módulos criados
from slack_utils import SlackBot
from message_reader import MessageReader

def main():
    """Função principal do bot"""
    print("Iniciando Slack Bot...")
    
    # Inicializa o bot e o leitor de mensagens
    bot = SlackBot()
    reader = MessageReader()
    
    # Canais reais do seu workspace (sem # pois o Slack usa IDs)
    canais_reais = ['teste', 'toda-a-empresa-slack', 'social', 'novo-canal']
    
    print("\n=== ADICIONANDO BOT AOS CANAIS ===")
    for canal in canais_reais:
        print(f"Tentando adicionar bot ao canal #{canal}...")
        bot.adicionar_bot_ao_canal(canal)
    
    print("\n=== TESTANDO CANAIS REAIS ===")
    resultados = reader.testar_canais_disponiveis(canais_reais)
    
    if resultados:
        print(f"\nEncontrados {len(resultados)} canais com mensagens!")
        
        # Testa busca por ID do usuário (U09P08RF11P = pedro.soares)
        print("\n=== BUSCANDO MENSAGENS DO USUÁRIO U09P08RF11P ===")
        mensagens_usuario = reader.buscar_mensagens_por_usuario('#teste', 'U09P08RF11P', limite=20)
        
        if mensagens_usuario:
            print("Mensagens do usuário U09P08RF11P encontradas!")
        else:
            print("Mensagens do usuário U09P08RF11P não encontradas.")
        
        # Testa busca por texto "teste de contexto"
        print("\n=== BUSCANDO MENSAGEM 'TESTE DE CONTEXTO' ===")
        mensagens_contexto = reader.buscar_mensagens_por_texto('#teste', 'teste de contexto', limite=20)
        
        if mensagens_contexto:
            print("Mensagem 'teste de contexto' encontrada!")
        else:
            print("Mensagem 'teste de contexto' não encontrada.")
        
        # Testa busca por texto "testeta" (mensagem mais recente)
        print("\n=== BUSCANDO MENSAGEM 'TESTETA' ===")
        mensagens_testeta = reader.buscar_mensagens_por_texto('#teste', 'testeta', limite=20)
        
        if mensagens_testeta:
            print("Mensagem 'testeta' encontrada!")
        else:
            print("Mensagem 'testeta' não encontrada.")
    else:
        print("Nenhum canal encontrado com mensagens.")
    
    # Testa envio de mensagem
    print("\n=== TESTANDO ENVIO DE MENSAGEM ===")
    sucesso = bot.enviar_mensagem('#teste', 'Bot funcionando! Mensagem de teste.')
    
    if sucesso:
        print("Bot configurado e funcionando perfeitamente!")
    else:
        print("Erro ao enviar mensagem de teste.")

if __name__ == "__main__":
    main()
