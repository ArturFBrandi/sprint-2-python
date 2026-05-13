# Sistema de Câmera Inteligente com OCR
# Sprint 2 - Pensamento Computacional com Python
# Simulação de detecção de texto via câmera para estudantes universitários

import urllib.parse

# Lista que armazena o histórico de capturas OCR feitas na sessão
historico_capturas = []


def exibir_menu():
    print("\n" + "=" * 52)
    print("       CÂMERA INTELIGENTE COM OCR")
    print("=" * 52)
    print("  1. Simular captura de texto (OCR)")
    print("  2. Pesquisar texto capturado no Google")
    print("  3. Traduzir texto capturado")
    print("  4. Visualizar histórico de capturas")
    print("  5. Limpar histórico")
    print("  0. Sair")
    print("=" * 52)


def simular_captura_ocr():
    """Simula a detecção de texto via câmera (OCR)."""
    print("\n--- SIMULAÇÃO DE CAPTURA OCR ---")
    print("Aponte a câmera para um texto.")
    print("(Em um app real, o OCR detectaria automaticamente)\n")

    texto = input("Digite o texto que seria detectado pela câmera: ").strip()

    if not texto:
        print("[!] Nenhum texto detectado. Insira um conteúdo válido.")
        return

    if len(texto) < 3:
        print("[!] Texto muito curto para ser processado pelo OCR.")
        return

    print("\nQual o tipo de fonte detectada?")
    print("  1. Texto impresso (livro, documento)")
    print("  2. Lousa ou slide de aula")
    print("  3. Anotação manuscrita")

    while True:
        tipo_opcao = input("Selecione o tipo (1-3): ").strip()
        if tipo_opcao in ("1", "2", "3"):
            break
        print("[!] Opção inválida. Escolha 1, 2 ou 3.")

    tipos = {"1": "Texto impresso", "2": "Lousa/Slide", "3": "Manuscrito"}
    tipo = tipos[tipo_opcao]

    captura = {"texto": texto, "tipo": tipo}
    historico_capturas.append(captura)

    print(f"\n[✓] Texto capturado com sucesso!")
    print(f"    Conteúdo  : \"{texto}\"")
    print(f"    Tipo      : {tipo}")
    print(f"    Capturas  : {len(historico_capturas)} registro(s) no histórico")


def selecionar_captura(acao: str):
    """Exibe o histórico e retorna a captura escolhida pelo usuário."""
    if not historico_capturas:
        print("[!] Nenhum texto capturado ainda. Use a opção 1 primeiro.")
        return None

    print(f"\nTextos disponíveis para {acao}:")
    for i, captura in enumerate(historico_capturas, 1):
        resumo = captura["texto"][:45] + ("..." if len(captura["texto"]) > 45 else "")
        print(f"  {i}. [{captura['tipo']}] {resumo}")

    while True:
        escolha = input(f"\nEscolha um texto (1-{len(historico_capturas)}): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(historico_capturas):
            return historico_capturas[int(escolha) - 1]
        print(f"[!] Entrada inválida. Digite um número entre 1 e {len(historico_capturas)}.")


def pesquisar_no_google():
    """Gera um link de pesquisa no Google para o texto capturado."""
    print("\n--- PESQUISAR NO GOOGLE ---")

    captura = selecionar_captura("pesquisa")
    if captura is None:
        return

    texto = captura["texto"]
    query_encoded = urllib.parse.quote(texto)
    url = f"https://www.google.com/search?q={query_encoded}"

    print(f"\n[✓] Link de pesquisa gerado!")
    print(f"    Texto : \"{texto}\"")
    print(f"    URL   : {url}")
    print("\n(Em um app real, o navegador abriria automaticamente)")


def traduzir_texto():
    """Gera um link do Google Translate para o texto capturado."""
    print("\n--- TRADUZIR TEXTO ---")

    captura = selecionar_captura("tradução")
    if captura is None:
        return

    idiomas = {
        "1": ("Inglês",   "en"),
        "2": ("Espanhol", "es"),
        "3": ("Francês",  "fr"),
        "4": ("Alemão",   "de"),
    }

    print("\nIdioma de destino:")
    for chave, (nome, _) in idiomas.items():
        print(f"  {chave}. {nome}")

    while True:
        opcao = input("Selecione o idioma (1-4): ").strip()
        if opcao in idiomas:
            break
        print("[!] Opção inválida. Escolha entre 1 e 4.")

    nome_idioma, codigo = idiomas[opcao]
    texto = captura["texto"]
    texto_encoded = urllib.parse.quote(texto)
    url = f"https://translate.google.com/?sl=auto&tl={codigo}&text={texto_encoded}&op=translate"

    print(f"\n[✓] Link de tradução gerado!")
    print(f"    Texto original : \"{texto}\"")
    print(f"    Traduzir para  : {nome_idioma}")
    print(f"    URL            : {url}")
    print("\n(Em um app real, o Google Translate abriria com o texto já carregado)")


def visualizar_historico():
    """Exibe todos os textos capturados na sessão."""
    print("\n--- HISTÓRICO DE CAPTURAS ---")

    if not historico_capturas:
        print("Nenhum texto capturado ainda.")
        return

    print(f"\nTotal de registros: {len(historico_capturas)}\n")
    for i, captura in enumerate(historico_capturas, 1):
        print(f"  [{i}] Tipo  : {captura['tipo']}")
        print(f"       Texto : \"{captura['texto']}\"")
        print()


def limpar_historico():
    """Remove todos os registros do histórico após confirmação."""
    print("\n--- LIMPAR HISTÓRICO ---")

    if not historico_capturas:
        print("O histórico já está vazio.")
        return

    confirmacao = input(
        f"Remover {len(historico_capturas)} captura(s) do histórico? (s/n): "
    ).strip().lower()

    if confirmacao == "s":
        historico_capturas.clear()
        print("[✓] Histórico limpo com sucesso.")
    else:
        print("Operação cancelada.")


def main():
    print("\nBem-vindo ao Sistema de Câmera Inteligente com OCR!")
    print("Simule a detecção de textos e realize ações contextuais.")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                simular_captura_ocr()
            case "2":
                pesquisar_no_google()
            case "3":
                traduzir_texto()
            case "4":
                visualizar_historico()
            case "5":
                limpar_historico()
            case "0":
                print("\nEncerrando o sistema. Até logo!")
                break
            case _:
                print("\n[!] Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    main()
