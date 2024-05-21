# Extração de features em documentos com Azure Cognitive Service

Este projeto tem como objetivo demonstrar a criação de uma feature que faça a extração de dados de documentos utilizando os modelos de IA/ML da Azure através da utilização do **Azure Cognitive Service**.

## Execução do projeto

* Crie uma conta na Azure: https://portal.azure.com/
* Acesse o terminal do cloud shell e execute os comandos do arquivo `infra_as_code.azcli` ou utilizando o VSCode com a extensão do Azure CLI.
* Execute cada linha de comando do arquivo, uma a uma.
* Obtenha as informações de:
    * String de conexão do azure service bus
    * String de conexão do azure blob storage
* Atualize os arquivos .env dos modulos da API e do Handler
* Rode o projeto da API via Debuger do visual studio code, ou rode o comando `python .\api\app.py`
* Rode o projeto do EventHandler via Debuger do visual studio code, ou rode o comando `python .\handler\extraction_features\app.py`

## Arquitetura do Projeto

A arquitetura da solução é composta por:

* API: Disponibiliza os endpoints para enviar um arquivo, validar o status de processamento e obter o retorno
* EventHandler: Para executar o processamento da operação mediando execuçaõ baseada em evento
* Azure Storage Account: Para persistir os documentos de entrada e saída
* Azure Event Grid: Para interceptar o momento que o documento é gerado no diretorio de input
* Azure Service Bus Queue: Para propagar o evento de à ser processado