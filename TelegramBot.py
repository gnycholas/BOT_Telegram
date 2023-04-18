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

# Defina o horário em que a enquete será enviada (no formato HH:MM)
horario_envio = '19:30'

def remove_bom_from_csv(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    content_no_bom = content.replace('\ufeff', '')

    with codecs.open(filename, 'w', encoding='utf-8') as file:
        file.write(content_no_bom)
        
async def get_random_question():
    # Remova o BOM do arquivo CSV
    remove_bom_from_csv('questoes.csv')

    # Abra o arquivo CSV com as questões
    with open('questoes.csv', 'r', encoding='utf-8') as csvfile:
        # Crie um leitor de CSV
        reader = csv.DictReader(csvfile, delimiter=';')

        # Converta o CSV em uma lista
        questoes = [row for row in reader]

        # Selecione uma pergunta aleatória
        row = random.choice(questoes)
        pergunta = row["'pergunta'"].strip("'")
        opcoes = [row["'opcao_1'"].strip("'"), row["'opcao_2'"].strip("'"), row["'opcao_3'"].strip("'"), row["'opcao_4'"].strip("'")]
        resposta_correta = int(row["'resposta_correta'"].strip("'"))
        explicacao = row["'explicacao'"].strip("'")
        return pergunta, opcoes, resposta_correta, explicacao


async def enviar_enquete_e_explicacao():
    # Obtenha uma pergunta aleatória do arquivo CSV
    pergunta, opcoes, resposta_correta, explicacao = await get_random_question()

    # Envie a enquete
    poll = await bot.send_poll(chat_id='-826531161', question=pergunta, options=opcoes, correct_option_id=resposta_correta, explanation=explicacao, type="quiz")

async def main():
    while True:
        agora = datetime.datetime.now().strftime('%H:%M')
        if agora == horario_envio:
            # Aguardar a função enviar_enquete_e_explicacao() ser concluída antes de continuar
            await enviar_enquete_e_explicacao()
            # Aguardar um minuto antes de verificar o horário novamente
            await asyncio.sleep(60)

# Iniciar o loop de eventos da biblioteca asyncio
asyncio.run(main())
