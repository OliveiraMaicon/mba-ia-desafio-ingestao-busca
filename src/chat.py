from search import search

def main():
    print("Bem-vindo ao chat! Faça sua pergunta sobre o documento. Digite 'sair' para terminar.")
    while True:
        question = input("Sua pergunta: ")
        if question.lower() == 'sair':
            break
        response = search(question)
        print("\nResposta:", response.content)
        print("-" * 20)


if __name__ == "__main__":
    main()