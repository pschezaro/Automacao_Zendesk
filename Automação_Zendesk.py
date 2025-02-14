import requests
import json
import time

# Configurações do Zendesk
SUBDOMINIO = "*************"
EMAIL = "sysapi@linktelwifi.com/token"
TOKEN = "****************************************"
HEADERS = {"Content-Type": "application/json"}

# URL da API do Zendesk
URL_TICKETS = f"https://{SUBDOMINIO}.zendesk.com/api/v2/tickets/create_many.json"
URL_SEARCH_USER = f"https://{SUBDOMINIO}.zendesk.com/api/v2/users/search.json?query="

# Dados comuns dos chamados
ASSUNTO = "Massiva - Instabilidade no serviço"
DESCRICAO = "Estamos cientes de uma instabilidade afetando o serviço e já estamos trabalhando para resolver."

# Campos personalizados do Zendesk (IDs precisam ser atualizados conforme sua conta)
ID_TELEFONE = 360039303732
ID_RECLAMANTE = 360039302832

# ID da organização "Prefeitura de Itapevi"
ORGANIZATION_ID = "361186918231"
GROUP_ID = "360012919412"

# Lista de clientes
clientes = [
    {"name": "USF/UBS JD. Vitapolis"},
    {"name": "Centro de Referencia da Mulher"},
    {"name": "Galpao da Secretaria de Educação CLI"},
    {"name": "Centro de Referência da Mulher"},
    {"name": "Resolve Facil Novo Ponto"},
    {"name": "CEMEB Maria Angela Neves"},
    {"name": "Escola Municipal Livre de Musica"},
    {"name": "CEMEB Dona Maria Roncagli Michelotti"},
    {"name": "CEMEB Mario Thomas Oliveira"},
    {"name": "Resolve Facil Hotspot"},
    {"name": "Base da Guarda Municipal - Itaqui"},
    {"name": "Galpao da Prefeitura no CLI"},
    {"name": "Secretaria da Saude"},
    {"name": "Central de Resgate - SAMU"},
    {"name": "Pronto Socorro Central - Infantil"},
    {"name": "Canil - Base"},
    {"name": "Sede da Prefeitura - Nova"},
    {"name": "Vigilancia Sanitaria"},
    {"name": "Conselho Tutelar"},
    {"name": "CEMEB Dra. Zilda Arns Neumann"},
    {"name": "CEMEB Cecila Belli - Pica Pau"},
    {"name": "CEMEB Dimaraes Antonio Sandei"},
    {"name": "CEMEB Prof. Paulo Freire"},
    {"name": "Secretaria do Meio Ambiente"},
    {"name": "Secretaria de Administracao e Tecnologia"},
    {"name": "USF Jardim Sao Carlos"},
    {"name": "Praca Joao Batista Silveira"},
    {"name": "ItapeviPrev"},
    {"name": "CAPS II - Centro de Atencao Psicossocial Espaco Conviver"},
    {"name": "Administracao Parque Municipal Itapevi"},
    {"name": "Praca Parque Novo Itapevi - Poste 1"},
    {"name": "Praca Parque Novo Itapevi - Poste 2"},
    {"name": "Praca Estadio Municipal"},
    {"name": "Praca Parque Novo Itapevi - Poste 3"},
    {"name": "Praca Estadio Municipal"},
    {"name": "Relogio de Ponto"},
    {"name": "Pronto Socorro Michelotte 2"},
    {"name": "Centro de Zoonoses"},
    {"name": "Unifarma - PS Infantil"},
    {"name": "Centro de Referencia da Mulher"},
    {"name": "COI PS Central"},
    {"name": "Pronto Socorro Central - Jose Michelotte"},
    {"name": "CRAS Vila Cardoso"},
    {"name": "PS Levi de Lima"},
    {"name": "CEMEB Neusa Marques Lobato"},
    {"name": "UBS Vila Cardoso"},
    {"name": "CEMEB Antonio Frederico de Castro Alves"},
    {"name": "USF Chacara Santa Cecilia"},
    {"name": "CEMEB Manuel Bandeira"},
    {"name": "CEMEB Maestro Gilberto de Pinho"},
    {"name": "USF Jardim Briquet"},
    {"name": "CEMEB Dorina de Gouvea Nowill"},
    {"name": "CEMEB Manuel Bandeira"},
    {"name": "CEMEB Marcilene Luiza de Melo Gazolla"},
    {"name": "CEMEB Cecilia Meireles"},
    {"name": "CEMEB Magali Trevizan Proenca de Almeida"},
    {"name": "CEMEB Antonio Carlos Gomes"},
    {"name": "Unifarma - UBS Cardoso"},
    {"name": "CCI - Centro de Idoso"},
    {"name": "UBS Unifarma - Santa Cecilia"},
    {"name": "Velorio Municipal"},
    {"name": "Praca Nelson Mandela"},
    {"name": "Unifarma - UBS Jardim Briquet"},
    {"name": "CEMEB Emilia Rossi Luigi"},
    {"name": "CEMEB Dona Floriza Nunes de Camargo"},
    {"name": "USF Jardim Rosemeire"},
    {"name": "CRAS Vila Aurora"},
    {"name": "CEMEB Carlos Drummond de Andrade"},
    {"name": "Unifarma - USF Jardim Rosemeire"},
    {"name": "CEMEB Professor Paulo Mariano de Arruda"},
    {"name": "CEMEB Prof Eneide Aparecida"},
    {"name": "Farmacia UBS Rainha"},
    {"name": "UBS Rainha"},
    {"name": "CEMEB Prof Florestan Fernandes"},
    {"name": "USF Parque Suburbano"},
    {"name": "Praca Ginasio de Esporte"},
    {"name": "Secretaria de Desenvolvimento Social e Cidadania"},
    {"name": "Secretaria de Cultura e Juventude"},
    {"name": "Base da Guarda do Terminal Rodoviario Central"},
    {"name": "CEMEB Prof Christel Ruth Lung Roosch"},
    {"name": "Terminal Central de Onibus"},
    {"name": "CEMEB Maria Clara Machado"},
    {"name": "Ginasio de Esportes"},
    {"name": "Farmacia UBS Suburbano"},
    {"name": "CEMEB Dr. Antonio Manoel de Oliveira"},
    {"name": "Praca do Povo"},
    {"name": "Secretaria de Educacao"},
    {"name": "Praca do Nordestino"},
    {"name": "Praca 18 de Fevereiro"},
    {"name": "Centro POP"},
    {"name": "Escola de Tempo Integral Tarsila do Amaral"},
    {"name": "CAPS II - Infanto Juvenil Ciranda"},
    {"name": "COI Divisa de Cotia - Entrada da Cidade"},
    {"name": "Teatro Municipal"},
    {"name": "CEMEB Santa Paula Cerioli"},
    {"name": "CEMEB Joao Guimaraes Rosa"},
    {"name": "CEMEB Prof Benedito Antonio dos Santos"},
    {"name": "CEMEB Governador Andre Franco Montoro"},
    {"name": "Posto Base da Guarda Municipal - Cardoso"},
    {"name": "CEMEB Papa Joao Paulo II"},
    {"name": "Escola do Futuro - ETI Padre Giovanni Cornaro"},
    {"name": "UBS Jardim Santa Rita 2"},
    {"name": "CEMEB Rui Barbosa"},
    {"name": "CEMEB Vinicius de Moraes"},
    {"name": "UBS Jardim Santa Rita 1"},
    {"name": "Escola do Futuro - Irany Toledo de Moraes"},
    {"name": "CEMEB Antonio Goncalves Dias"},
    {"name": "Secretaria de Obras"},
    {"name": "CEMEB Vereador Ubiratan Chaluppe"},
    {"name": "CEMEB Professora Viviane Maria de David de Abreu"},
    {"name": "CEMEB Presidente Tancredo de Almeida Neves"},
    {"name": "CEMEB Eduardo Joao da Silva"},
    {"name": "UBS Vila Gioia"},
    {"name": "CEMEB Francisco Laercio Nogueira Lins"},
    {"name": "Unifarma - PS Santa Rita"},
    {"name": "Unifarma - UBS Jd. Santa Rita II"},
    {"name": "Arquivo Geral"},
    {"name": "USF Vila Gioia"},
    {"name": "CIS - Centro Integrado de Especialidades"},
    {"name": "Forum Municipal"},
    {"name": "COI - Secretaria de Seguranca"},
    {"name": "CEMEB Prof. Jossei Toda"},
    {"name": "CRAS Maristela"},
    {"name": "Cemiterio Memorial Parque"},
    {"name": "Escola de Tempo Integral da Cohab"},
    {"name": "CEMEB Monteiro Lobato"},
    {"name": "Secretaria de Esportes Alto da Colina"},
    {"name": "CEMEB Maria Zibina de Carvalho"},
    {"name": "CEMEB Jose dos Santos Novaes"},
    {"name": "Unifarma - UBS Alto da Colina"},
    {"name": "UBS Cohab"},
    {"name": "UBS Dr. Flavio Piovesan"},
    {"name": "CEMEB Bem Vindo Moreira Nery"},
    {"name": "CEMEB Antonio Oliveira Cunha"},
    {"name": "Escola 5.0 de Idiomas"},
    {"name": "CEMEB Cora Coralina"},
    {"name": "CEMEB Carlos Ramiro de Castro"},
    {"name": "COI Centro Comercial Cohab"},
    {"name": "CEMEB Maestro Heitor Villa Lobos"},
    {"name": "Centro de Reabilitacao"},
    {"name": "CIE Alto da Colina"},
    {"name": "CEMEB Candido Portinari"},
    {"name": "CEF Parque da Cohab"},
    {"name": "CEMEB Vereador Antonio Rodrigues"},
    {"name": "Unifarma - UBS Cohab"},
    {"name": "UBS Ambuita"},
    {"name": "CEMEB Prof Edevaldo Caramez"},
    {"name": "Secretaria da Fazenda"},
    {"name": "Divisao de Frota"},
    {"name": "Demutran Dep. de Transporte"},
    {"name": "USF Ambuita"},
    {"name": "CEMEB Manoela Sanches Casagrande"},
    {"name": "Secretaria de Desenvolvimento"},
    {"name": "CREAS - SASC"},
    {"name": "CEMEB Jornalista Joao Valerio de Paula Neto"},
    {"name": "CRAS Amador Bueno"},
    {"name": "CEMEB Maria Jose Faria Biagione"},
    {"name": "Posto da Guarda Municipal - Amador Bueno"},
    {"name": "CEMEB Vereador Roberval Luiz Mendes da Silva"},
    {"name": "CEMEB Prof Alice Celestino Izabo Ramari"},
    {"name": "CEMEB Associacao Apecatu"},
    {"name": "CEMEB Evany Camargo Ribeiro"},
    {"name": "UBS Amador Bueno"},
    {"name": "ETI Padre Gerald Cluskey"},
    {"name": "CEMEB Prof Rosana Minani Andrade"},
    {"name": "Praca Paulo Franca Amador Bueno"},


]

# Função para buscar usuário no Zendesk dentro da organização
def buscar_usuario(nome_cliente):
    url = f"{URL_SEARCH_USER}{nome_cliente}"
    response = requests.get(url, headers=HEADERS, auth=(EMAIL, TOKEN))

    if response.status_code == 200:
        users = response.json().get("users", [])
        for user in users:
            if user.get("name") == nome_cliente and str(user.get("organization_id")) == ORGANIZATION_ID:
                print(f"✅ Usuário encontrado: {nome_cliente} (ID: {user.get('id')})")
                return user.get("id")  # Retorna o ID do usuário existente

    print(f"❌ Usuário não encontrado: {nome_cliente}")
    return None  # Retorna None se o usuário não for encontrado

# Criando tickets sem duplicar usuários
tickets_data = {"tickets": []}

for cliente in clientes:
    nome_cliente = cliente["name"]
    usuario_id = buscar_usuario(nome_cliente)

    ticket = {
        "subject": ASSUNTO,
        "comment": {"body": f"Olá {nome_cliente},\n\n{DESCRICAO}"},
        "organization_id": ORGANIZATION_ID,
        "group_id": GROUP_ID,
        "priority": "high",
        "status": "open",  # Define o status como "Aberto"
        "custom_fields": [
            {"id": ID_TELEFONE, "value": "1121977040"},
            {"id": ID_RECLAMANTE, "value": "Suporte"}
        ]
    }

    # Se o usuário já existe, usa o ID dele
    if usuario_id:
        ticket["requester_id"] = usuario_id
    else:
        ticket["requester"] = {"name": nome_cliente, "organization_id": ORGANIZATION_ID}  # Cria um novo usuário apenas se necessário

    tickets_data["tickets"].append(ticket)

# Enviar requisição para o Zendesk
response = requests.post(URL_TICKETS, headers=HEADERS, auth=(EMAIL, TOKEN), data=json.dumps(tickets_data))

# Verifica resposta e busca os IDs dos chamados criados
if response.status_code in [200, 201]:
    response_data = response.json()
    job_status = response_data.get("job_status", {})
    job_id = job_status.get("id")

    print(f"✅ Chamados enviados com sucesso! ID do job: {job_id}")
    print("🔄 Aguardando criação dos chamados...")

    # URL para verificar o status do job
    job_url = f"https://{SUBDOMINIO}.zendesk.com/api/v2/job_statuses/{job_id}.json"

    while True:
        job_response = requests.get(job_url, headers=HEADERS, auth=(EMAIL, TOKEN))
        job_data = job_response.json()
        status = job_data.get("job_status", {}).get("status")

        if status == "completed":
            results = job_data.get("job_status", {}).get("results", [])

            if results and "id" in results[0]:
                ticket_ids = [result["id"] for result in results]
                print("🎫 Chamados criados com sucesso!")
                for i, ticket_id in enumerate(ticket_ids):
                    print(f"📌 Cliente: {clientes[i]['name']} → Ticket ID: {ticket_id} (Status: Aberto)")
            else:
                print("❌ Nenhum ID de ticket encontrado na resposta. Verifique a estrutura do retorno.")

            break
        elif status == "failed":
            print("❌ Falha ao criar alguns chamados.")
            break

        time.sleep(2)  # Aguarda 2 segundos antes de consultar novamente

else:
    print(f"❌ Erro ao criar tickets: {response.status_code}")
    print(response.text)
