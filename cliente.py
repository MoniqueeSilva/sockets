import socket
from colorama import Fore, Style # Biblioteca para adicionar cores no terminal do cliente

def main():
    # Configurações do servidor IP e porta
    server_ip = "127.0.0.1"
    port = 8001
    
    # Cria um socket TCP-IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor
    client_socket.connect((server_ip, port))
    
    # Recebe a lista de itens disponíveis na loja
    lista_itens = client_socket.recv(1024).decode("utf-8")
    print("Lista de Itens disponíveis na loja:")
    print(lista_itens)
    
    # Solicita ao cliente que escolha os itens para compra
    carrinho = {}
    while True:
        produto = input("Digite o nome do produto que deseja comprar (ou digite 'fim' para encerrar): ").strip()
        if produto.lower() == 'fim':
            break
        quantidade = int(input("Digite a quantidade desejada: "))
        carrinho[produto] = quantidade
    
    # Envia o carrinho para o servidor
    carrinho_str = str(carrinho)
    client_socket.send(carrinho_str.encode("utf-8"))
    
    # Recebe o total da compra
    total_compra = client_socket.recv(1024).decode("utf-8")
    print(Fore.YELLOW + f"Total da compra: R${total_compra}")
    
    # Confirma o pagamento ou cancelamento da compra
    confirmacao = input(Fore.WHITE +'Digite ' + Fore.GREEN + '(p) ' + Fore.WHITE + 'para confirmar ou ' + Fore.RED + '(c) ' + Fore.WHITE + 'para cancelar: ').strip()
    client_socket.send(confirmacao.encode("utf-8"))

    # Receber mensagem de agradecimento do servidor
    msg_agradecimento = client_socket.recv(1024).decode("utf-8")
    print(Fore.MAGENTA + msg_agradecimento)
    
    # Fecha o socket do cliente
    client_socket.close()

if __name__ == "__main__":
    main()
