import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_score, recall_score, \
    f1_score
from sklearn.preprocessing import OneHotEncoder
import re

#Abrir o log e extrair os dados e retornar um df
def processar_log(log_file='score_log.txt'):
    with open(log_file, 'r') as file:
        txt = file.read()

    log_split = txt.split('\n\n')

    data = {
        'CurrentScore': [],
        'Action': [],
        'UpperCell': [],
        'LowerCell': [],
        'LeftCell': [],
        'RightCell': [],
    }

    for linha in log_split:
        match_score = re.search(r'Current Score: (\d+)', linha)
        match_action = re.search(r'Action: (\w+)', linha)
        match_upper = re.search(r'UpperCell: (\w+)', linha)
        match_lower = re.search(r'LowerCell: (\w+)', linha)
        match_left = re.search(r'LeftCell: (\w+)', linha)
        match_right = re.search(r'RightCell: (\w+)', linha)

        if all(match is not None for match in
               [match_score, match_action, match_upper, match_lower, match_left, match_right]):
            data['CurrentScore'].append(int(match_score.group(1)))
            data['Action'].append(match_action.group(1))
            data['UpperCell'].append(match_upper.group(1))
            data['LowerCell'].append(match_lower.group(1))
            data['LeftCell'].append(match_left.group(1))
            data['RightCell'].append(match_right.group(1))

    df = pd.DataFrame(data)

    return df


def prepare_input_for_model(df):
    # Selecionar as colunas relevantes, incluindo 'Pontuação Ponderada'

    # tirar current score e heuristica
    features = df[['UpperCell', 'LowerCell', 'LeftCell', 'RightCell', 'Heuristica']]
    return features

def train_and_evaluate_model(df):
    # Calcular Pontuações Ponderadas para Cada Ação
    df['Heuristica'] = 0  # Inicialmente, todas as pontuações ponderadas são 0

    # Pesos temporarios para cada ação
    heuristica_lixo_correto = 20 # Peso para a regra de apanhar lata correta
    heuristica_lixo_incorreto = -20  # Peso para a regra de apanhar lata incorreta
    heuristica_bater_parede = -40  # Peso para a regra de colisão com a parede
    heuristica_movimentos_sem_ponto = -5

    for i in range(len(df)):
        row = df.iloc[i]

       # Logica para tentar obter a pontuação máxima - IA
        if row['Action'] in ['E', 'up', 'down', 'left', 'right']:
            if row['Action'] == 'E':
                if 'garbage' in [row['UpperCell'], row['LowerCell'], row['LeftCell'], row['RightCell']]:
                    df.at[i, 'Heuristica'] += heuristica_lixo_correto
                else:
                    df.at[i, 'Heuristica'] += heuristica_lixo_incorreto

            elif row['Action'] in ['up', 'down', 'left', 'right']:
                if row['Action'] == 'up' and row['UpperCell'] == 'wall':
                    df.at[i, 'Heuristica'] += heuristica_bater_parede

                elif row['Action'] == 'down' and row['LowerCell'] == 'wall':
                    df.at[i, 'Heuristica'] += heuristica_bater_parede

                elif row['Action'] == 'left' and row['LeftCell'] == 'wall':
                    df.at[i, 'Heuristica'] += heuristica_bater_parede

                elif row['Action'] == 'right' and row['RightCell'] == 'wall':
                    df.at[i, 'Heuristica'] += heuristica_bater_parede

        else:
            df.at[i, 'Heuristica'] += heuristica_movimentos_sem_ponto


    # Preparar os dados para o modelo Naive Bayes
    X = prepare_input_for_model(df)
    y = df['Action']

    # One-hot encoding para colunas categóricas em X
    # Aqui transformamos cada coluna C em binária
    encoder = OneHotEncoder()
    X_encoded = encoder.fit_transform(X)

    # Dividir os dados em conjuntos - 25% teste e 75% treino
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.25, random_state=90)

    # Inicializar e treinar o modelo - Naive Bayes Multimonial deu melhores resultados que o Gaussian
    model = MultinomialNB()
    model.fit(X_train.toarray(), y_train)

    # Fazer previsões nos dados de teste
    y_pred = model.predict(X_test.toarray())

    print('\n')
    # Calcular a precisão do modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy do modelo: {accuracy}')

    print('\n')
    # DataFrame com as ações reais e previstas
    df_predicoes = pd.DataFrame({'Ação Real': y_test, 'Ação Prevista': y_pred})

    y_pred = model.predict(X_test)

    print('\n')
    # Calcular as métricas de avaliação
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    confusion = confusion_matrix(y_test, y_pred)

    print(f'Accuracy: {accuracy}')
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
    print(f'F1 Score: {f1}')
    print('Confusion Matrix:')
    print(confusion)
    return df['Action']

# Exemplo de uso da função
df = processar_log('score_log.txt')
actions = train_and_evaluate_model(df)
print('\n')
print("Distribuição de frequência")
print(df['Action'].value_counts())


