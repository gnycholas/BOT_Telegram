import csv

# Leia as questões do arquivo CSV e imprima as informações na tela
with open('questoes.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print("Pergunta:", row['\ufeffpergunta'])
        opcoes = [row['opcao_1'], row['opcao_2'], row['opcao_3'], row['opcao_4']]
        print("Opções:", ",".join(opcoes))
        print("Resposta correta:", int(row['resposta_correta']))
        print("Explicação:", row['explicacao'])
        print("\n")
