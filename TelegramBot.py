import telegram
import datetime
import asyncio
import random
import csv
import codecs

# Defina o token do seu bot
TOKEN = '5434640983:AAEr5Swzwl8Bul8Wfd7NZNr6MYZGwmI4pvs'

# Crie uma instância do bot
bot = telegram.Bot(token=TOKEN)

# Defina os horários em que as enquetes serão enviadas (no formato HH:MM)
horarios_envio = ['23:18', '23:20']

ultimo_dia = None
proximo_horario = 0

def remove_bom_from_csv(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    content_no_bom = content.replace('\ufeff', '')

    with codecs.open(filename, 'w', encoding='utf-8') as file:
        file.write(content_no_bom)

async def get_next_question():
    # Remova o BOM do arquivo CSV
    remove_bom_from_csv('questoes.csv')

    # Abra o arquivo CSV com as questões
    with open('questoes.csv', 'r', encoding='utf-8') as csvfile:    
        # Crie um leitor de CSV
        reader = csv.DictReader(csvfile, delimiter=';')

        # Converta o CSV em uma lista
        questoes = [row for row in reader]

        # Leia o índice da próxima pergunta do arquivo 'next_question_index.txt'
        with open('next_question_index.txt', 'r') as index_file:
            next_question_index = int(index_file.read().strip())

        # Atualize o índice da próxima pergunta e salve-o no arquivo
        next_question_index = (next_question_index + 1) % len(questoes)
        with open('next_question_index.txt', 'w') as index_file:
            index_file.write(str(next_question_index))

        # Selecione a pergunta de acordo com o índice
        row = questoes[next_question_index]
        pergunta = row["'pergunta'"].strip("'")
        opcoes = [row["'opcao_1'"].strip("'"), row["'opcao_2'"].strip("'"), row["'opcao_3'"].strip("'"), row["'opcao_4'"].strip("'")]
        resposta_correta = int(row["'resposta_correta'"].strip("'"))
        explicacao = row["'explicacao'"].strip("'")
        return pergunta, opcoes, resposta_correta, explicacao

async def enviar_enquete_e_explicacao():
    # Obtenha a próxima pergunta do arquivo CSV
    pergunta, opcoes, resposta_correta, explicacao = await get_next_question()

    # Envie a enquete
    poll = await bot.send_poll(chat_id='-826531161', question=pergunta, options=opcoes, correct_option_id=resposta_correta, explanation=explicacao, type="quiz")

async def main():
    global ultimo_dia, proximo_horario

    while True:
        agora = datetime.datetime.now()
        data_atual = agora.date()
        hora_atual = agora.strftime('%H:%M')

        if data_atual != ultimo_dia:
            ultimo_dia = data_atual
            proximo_horario = 0

        if hora_atual == horarios_envio[proximo_horario]:
            # Aguardar a função enviar_enquete_e_explicacao() ser concluída antes de continuar
            await enviar_enquete_e_explicacao()

            # Atualizar o próximo horário e aguardar um minuto antes de verificar o horário novamente
            proximo_horario = (proximo_horario + 1) % len(horarios_envio)
            await asyncio.sleep(60)

# Iniciar o loop de eventos da biblioteca asyncio
asyncio.run(main())
