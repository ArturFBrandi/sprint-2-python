# Sistema de Câmera Inteligente com OCR
# Sprint 3 - Pensamento Computacional com Python
# Simulação de detecção de texto via câmera para estudantes universitários

import urllib.parse

# Dicionários de apoio (dados fixos do domínio da aplicação)
TIPOS_FONTE = {"1": "Texto impresso", "2": "Lousa/Slide", "3": "Manuscrito"}

IDIOMAS = {
    "1": ("Inglês", "en"),
    "2": ("Espanhol", "es"),
    "3": ("Francês", "fr"),
    "4": ("Alemão", "de"),
}


def exibir_menu() -> None:
    """Renderiza o menu principal com todas as opções numeradas."""
    print("\n" + "=" * 52)
    print("       CÂMERA INTELIGENTE COM OCR")
    print("=" * 52)
    print("  1. Simular captura de texto (OCR)")
    print("  2. Pesquisar texto capturado no Google")
    print("  3. Traduzir texto capturado")
    print("  4. Visualizar histórico de capturas")
    print("  5. Ver estatísticas das capturas")
    print("  6. Limpar histórico")
    print("  0. Sair")
    print("=" * 52)


def texto_valido(texto: str) -> bool:
    """Retorna True se o texto capturado tiver pelo menos 3 caracteres úteis."""
    return len(texto.strip()) >= 3


def resumir_texto(texto: str, limite: int = 45) -> str:
    """Retorna `texto` truncado em `limite` caracteres, com reticências se necessário."""
    if len(texto) <= limite:
        return texto
    return texto[:limite] + "..."


def criar_captura(texto: str, tipo: str) -> dict:
    """Monta e retorna o dicionário que representa uma captura de OCR."""
    return {"texto": texto, "tipo": tipo}


def ler_tipo_fonte() -> str:
    """Solicita e valida em loop o tipo de fonte do texto capturado."""
    print("\nQual o tipo de fonte detectada?")
    for chave, nome in TIPOS_FONTE.items():
        print(f"  {chave}. {nome}")

    while True:
        opcao = input("Selecione o tipo (1-3): ").strip()
        if opcao in TIPOS_FONTE:
            return TIPOS_FONTE[opcao]
        print("[!] Opção inválida. Escolha 1, 2 ou 3.")


def simular_captura_ocr(historico: list) -> dict | None:
    """
    Simula a detecção de texto via câmera (OCR).

    Recebe o histórico de capturas por parâmetro, adiciona a nova captura
    validada e retorna o dicionário criado (ou None se o texto for inválido).
    """
    print("\n--- SIMULAÇÃO DE CAPTURA OCR ---")
    print("Aponte a câmera para um texto.")
    print("(Em um app real, o OCR detectaria automaticamente)\n")

    texto = input("Digite o texto que seria detectado pela câmera: ").strip()

    if not texto_valido(texto):
        print("[!] Texto inválido. Insira ao menos 3 caracteres.")
        return None

    tipo = ler_tipo_fonte()
    captura = criar_captura(texto, tipo)
    historico.append(captura)

    print("\n[✓] Texto capturado com sucesso!")
    print(f"    Conteúdo  : \"{texto}\"")
    print(f"    Tipo      : {tipo}")
    print(f"    Capturas  : {len(historico)} registro(s) no histórico")
    return captura


def indice_valido(escolha: str, tamanho: int) -> bool:
    """Retorna True se `escolha` for um índice numérico dentro do intervalo 1..tamanho."""
    return escolha.isdigit() and 1 <= int(escolha) <= tamanho


def selecionar_captura(historico: list, acao: str) -> dict | None:
    """Exibe o histórico e retorna a captura escolhida pelo usuário (ou None se vazio)."""
    if not historico:
        print("[!] Nenhum texto capturado ainda. Use a opção 1 primeiro.")
        return None

    print(f"\nTextos disponíveis para {acao}:")
    for i, captura in enumerate(historico, 1):
        resumo = resumir_texto(captura["texto"])
        print(f"  {i}. [{captura['tipo']}] {resumo}")

    while True:
        escolha = input(f"\nEscolha um texto (1-{len(historico)}): ").strip()
        if indice_valido(escolha, len(historico)):
            return historico[int(escolha) - 1]
        print(f"[!] Entrada inválida. Digite um número entre 1 e {len(historico)}.")


def montar_url_busca_google(texto: str) -> str:
    """Retorna a URL de pesquisa no Google para o texto informado."""
    query_encoded = urllib.parse.quote(texto)
    return f"https://www.google.com/search?q={query_encoded}"


def pesquisar_no_google(historico: list) -> None:
    """Gera e exibe a URL de pesquisa no Google para um texto do histórico."""
    print("\n--- PESQUISAR NO GOOGLE ---")

    captura = selecionar_captura(historico, "pesquisa")
    if captura is None:
        return

    url = montar_url_busca_google(captura["texto"])

    print("\n[✓] Link de pesquisa gerado!")
    print(f"    Texto : \"{captura['texto']}\"")
    print(f"    URL   : {url}")
    print("\n(Em um app real, o navegador abriria automaticamente)")


def ler_idioma_destino() -> tuple:
    """Solicita e valida em loop o idioma de destino da tradução."""
    print("\nIdioma de destino:")
    for chave, (nome, _) in IDIOMAS.items():
        print(f"  {chave}. {nome}")

    while True:
        opcao = input("Selecione o idioma (1-4): ").strip()
        if opcao in IDIOMAS:
            return IDIOMAS[opcao]
        print("[!] Opção inválida. Escolha entre 1 e 4.")


def montar_url_traducao(texto: str, idioma_codigo: str) -> str:
    """Retorna a URL do Google Translate para o texto e idioma informados."""
    texto_encoded = urllib.parse.quote(texto)
    return f"https://translate.google.com/?sl=auto&tl={idioma_codigo}&text={texto_encoded}&op=translate"


def traduzir_texto(historico: list) -> None:
    """Gera e exibe um link do Google Translate para um texto do histórico."""
    print("\n--- TRADUZIR TEXTO ---")

    captura = selecionar_captura(historico, "tradução")
    if captura is None:
        return

    nome_idioma, codigo = ler_idioma_destino()
    url = montar_url_traducao(captura["texto"], codigo)

    print("\n[✓] Link de tradução gerado!")
    print(f"    Texto original : \"{captura['texto']}\"")
    print(f"    Traduzir para  : {nome_idioma}")
    print(f"    URL            : {url}")
    print("\n(Em um app real, o Google Translate abriria com o texto já carregado)")


def visualizar_historico(historico: list) -> None:
    """Exibe todos os textos capturados na sessão."""
    print("\n--- HISTÓRICO DE CAPTURAS ---")

    if not historico:
        print("Nenhum texto capturado ainda.")
        return

    print(f"\nTotal de registros: {len(historico)}\n")
    for i, captura in enumerate(historico, 1):
        print(f"  [{i}] Tipo  : {captura['tipo']}")
        print(f"       Texto : \"{captura['texto']}\"")
        print()


def contar_capturas_por_tipo(historico: list) -> dict:
    """Retorna um dicionário {tipo_de_fonte: quantidade} a partir do histórico."""
    contagem = {}
    for captura in historico:
        tipo = captura["tipo"]
        contagem[tipo] = contagem.get(tipo, 0) + 1
    return contagem


def visualizar_estatisticas(historico: list) -> None:
    """Exibe a quantidade e o percentual de capturas agrupadas por tipo de fonte."""
    print("\n--- ESTATÍSTICAS DE CAPTURAS ---")

    if not historico:
        print("Nenhum texto capturado ainda. Não há estatísticas para exibir.")
        return

    contagem = contar_capturas_por_tipo(historico)
    total = len(historico)

    print(f"\nTotal de capturas: {total}\n")
    for tipo, quantidade in contagem.items():
        percentual = (quantidade / total) * 100
        print(f"  {tipo:<15}: {quantidade} ({percentual:.1f}%)")


def limpar_historico(historico: list) -> None:
    """Remove todos os registros do histórico após confirmação explícita."""
    print("\n--- LIMPAR HISTÓRICO ---")

    if not historico:
        print("O histórico já está vazio.")
        return

    confirmacao = input(
        f"Remover {len(historico)} captura(s) do histórico? (s/n): "
    ).strip().lower()

    if confirmacao == "s":
        historico.clear()
        print("[✓] Histórico limpo com sucesso.")
    else:
        print("Operação cancelada.")


def main() -> None:
    """Loop principal do programa; mantém o histórico local e roteia as opções do menu."""
    historico_capturas: list = []

    print("\nBem-vindo ao Sistema de Câmera Inteligente com OCR!")
    print("Simule a detecção de textos e realize ações contextuais.")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                simular_captura_ocr(historico_capturas)
            case "2":
                pesquisar_no_google(historico_capturas)
            case "3":
                traduzir_texto(historico_capturas)
            case "4":
                visualizar_historico(historico_capturas)
            case "5":
                visualizar_estatisticas(historico_capturas)
            case "6":
                limpar_historico(historico_capturas)
            case "0":
                print("\nEncerrando o sistema. Até logo!")
                break
            case _:
                print("\n[!] Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    main()
