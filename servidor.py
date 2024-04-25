import socket
import threading
from colorama import Fore, Style # Biblioteca para adicionar cores no terminal do servidor

# Função principal para executar o servidor
def run_server():

    # Cria um socket TCP-IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Configurações do servidor IP e porta
    server_ip = "127.0.0.1"
    port = 8001
    server_socket.bind((server_ip, port))
    
    # Escuta por conexões de entrada
    server_socket.listen(5)
    print(f"Servidor online em {server_ip}:{port}")

    while True:
        # Aceita uma nova conexão
        client_socket, client_address = server_socket.accept()
        
        # Cria uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Dicionário para armazenar os produtos e seus preços
produtos = {
    'HD': 100,
    'SSD': 200,
    'Memória RAM': 50,
    'Processador': 300,
    'Placa de vídeo': 400,
    'Fonte de alimentação': 80,
    'Cabo HDMI' : 50,
    'Teclado' : 100,
    'Mouse' : 40,
    'Fone' : 70,
    'WEBcam' : 30
}

# Variável global para armazenar o total acumulado de vendas
total_vendas = 0

# Dicionário que armazena o caixa acumulado para cada cliente
caixa_por_cliente = {}

# Função para enviar a lista de itens ao cliente
def enviar_lista(client_socket):
    lista_itens = "Itens disponíveis na loja:\n"
    for produto, preco in produtos.items():
        lista_itens += f"{produto}: R${preco}\n"
    client_socket.send(lista_itens.encode("utf-8"))

# Função para lidar com cliente
def handle_client(client_socket, client_address):
    global total_vendas
    global caixa_por_cliente
    
    print(f"Conexão aceita de {client_address[0]}:{client_address[1]}")

    # Envia a lista de itens disponíveis para o cliente
    enviar_lista(client_socket)
    
    # Recebe o carrinho do cliente
    carrinho_str = client_socket.recv(1024).decode("utf-8")
    carrinho = eval(carrinho_str)  # Converte string para dicionário
    
    # Calcula o total da compra
    total_compra = 0
    for produto, quantidade in carrinho.items():
        if produto in produtos:
            preco_produto = produtos[produto]
            total_compra += preco_produto * quantidade
    
    # Envia o total da compra para o cliente
    client_socket.send(str(total_compra).encode("utf-8"))
    
    # Recebe a confirmação ou cancelamento da compra
    confirmacao = client_socket.recv(1024).decode("utf-8")
    if confirmacao.lower() == "p":

        # Atualiza o total acumulado de vendas
        total_vendas += total_compra
        
        # Atualiza o caixa acumulado para o cliente
        if client_address in caixa_por_cliente:
            caixa_por_cliente[client_address] += total_compra
        else:
            caixa_por_cliente[client_address] = total_compra
        
        # Exibe o total de vendas acumulado
        print(Fore.GREEN + f"Total de vendas acumulado: R${total_vendas}")

        # Exibe o caixa acumulado para o cliente
        print(Fore.YELLOW + f"Caixa acumulado para o cliente {client_address}: R${caixa_por_cliente[client_address]}")
    else:
        print(Fore.RED + "Compra cancelada. Nenhum valor será acumulado.")

    # Envia uma mensagem de agradecimento ao cliente
    msg_agradecimento = "OBRIGADO PELA COMPRA!"
    client_socket.send(msg_agradecimento.encode("utf-8"))
    
    # Fecha o socket do cliente
    client_socket.close()

# Inicia o servidor
run_server()
