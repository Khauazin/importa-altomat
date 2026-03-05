import xml.etree.ElementTree as ET
import os

# ==============================
# CONFIGURAÇÕES
# ==============================
ENTRADA_FILE = "referencia.txt"        # TXT com data, hora e matricula:PIS
SAIDA_DIR = "xml_gerados_coletor_59"   # pasta onde os XMLs serão salvos
COD_EQUIPAMENTO = "59 - REP INOVA4"     # coletor
NATUREZA = "2"                          # tipo fixo
LIMITE_EVENTOS = 450                    # máximo de eventos por XML
# ==============================

os.makedirs(SAIDA_DIR, exist_ok=True)

def gerar_xml(eventos, indice):
    """Gera um arquivo XML com o bloco de eventos."""
    root = ET.Element("EVENTOS")
    for e_data in eventos:
        e = ET.SubElement(root, "EVENTO")
        ET.SubElement(e, "DATA_MOMENTO").text = e_data["data"]
        ET.SubElement(e, "HORA_MOMENTO").text = e_data["hora"]
        ET.SubElement(e, "COD_EQUIPAMENTO").text = COD_EQUIPAMENTO
        ET.SubElement(e, "IDENTIFICACAO").text = e_data["matricula"]
        ET.SubElement(e, "NATUREZA").text = NATUREZA

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    nome_saida = os.path.join(SAIDA_DIR, f"eventos_{indice:03}.xml")
    tree.write(nome_saida, encoding="utf-8", xml_declaration=False)
    print(f"✅ XML {indice:03} gerado com {len(eventos)} eventos → {nome_saida}")

def processar_arquivo():
    """Lê o arquivo de entrada e gera os XMLs."""
    eventos = []
    total_linhas = 0
    linhas_invalidas = 0

    with open(ENTRADA_FILE, "r", encoding="utf-8") as f:
        for num_linha, linha in enumerate(f, start=1):
            total_linhas += 1
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split()
            if len(partes) < 4:
                linhas_invalidas += 1
                print(f"⚠️ Linha {num_linha} ignorada (formato inválido): {linha}")
                continue

            data = partes[1]
            hora = partes[2]
            matricula_pis = partes[3]

            if ":" in matricula_pis:
                matricula, pis = matricula_pis.split(":", 1)
            else:
                matricula, pis = ("NAO_ENCONTRADO", matricula_pis)

            eventos.append({
                "data": data,
                "hora": hora,
                "matricula": matricula
            })

    # Confirma leitura
    print(f"\n📄 Total de linhas lidas: {total_linhas}")
    print(f"✔️ Linhas válidas: {len(eventos)}")
    print(f"⚠️ Linhas ignoradas: {linhas_invalidas}")

    # Gera os XMLs em blocos
    if not eventos:
        print("❌ Nenhum evento válido encontrado. Verifique o arquivo de entrada.")
        return

    for i in range(0, len(eventos), LIMITE_EVENTOS):
        bloco = eventos[i:i + LIMITE_EVENTOS]
        gerar_xml(bloco, i // LIMITE_EVENTOS + 1)

    print(f"\n🚀 Todos os arquivos XML foram gerados com sucesso!")
    print(f"📦 Total de eventos processados: {len(eventos)}")
    print(f"📁 Pasta de saída: {os.path.abspath(SAIDA_DIR)}")

if __name__ == "__main__":
    processar_arquivo()
