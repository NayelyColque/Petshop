import pyodbc  # pip install pyodbc
import pandas as pd  # pip install pandas
import os

try:
    dados_conexao = (
        "Driver={SQL Server};"
        "Server=DESKTOP-0JTQ3HI;"
        "Database=petshop;"
    )

    conn = pyodbc.connect(dados_conexao)
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()

except Exception as e:
    print("Erro na conexão com o banco de dados:", e)
    conexao = False
else:
    print("Conexão Estabelecida")
    conexao = True


while conexao:
    os.system("cls")
    print("""
|============================|       
|          Menu >-<          |
|============================|
|0 - Sair                    |
|1 - Cadastrar pet           |
|2 - Listar pets             |
|3 - Editar                  |
|4 - Excluir                 |
|============================|
""")
    try:
        escolha = int(input("Escolha uma opcao: "))
    except ValueError:
        print("Opção inválida.")
        continue

    os.system("cls")
    match escolha:
        case 0:
            conexao = False
        case 1:
            try:
                print("""\n
                    |============================|       
                    |        CADASTRAR PET       |
                    |============================|
                    """)
                tipo = input("Tipo.....: ")
                nome = input("Nome.....: ")
                idade = int(input("Idade....: "))
                cadastro = f"""
                INSERT INTO petshop (tipo_pet, nome_pet, idade)
                VALUES ('{tipo}', '{nome}', {idade})
                """
                inst_cadastro.execute(cadastro)
                conn.commit()
                print("Pet cadastrado com sucesso!")
            except ValueError:
                print("Erro: Idade deve ser um número!")
            
        case 2:
            lista_dados = []
            inst_consulta.execute("select * from petshop")
            data = inst_consulta.fetchall()
            for dt in data:
                lista_dados.append(dt)
            lista_dados = sorted(lista_dados)

            dados_df = pd.DataFrame.from_records(lista_dados, columns=['Id', 'Tipo', 'Nome', 'Idade'], index='Id')
            if dados_df.empty:
                print("Sem registros!")
            else:
                print(dados_df)
                print("\nDados listados")

        case 3:
            try:
                print("""\n
                    |============================|       
                    |         EDITAR PET         |
                    |============================|
                    """)
                pet_id = int(input("Digite o ID do pet que deseja editar: "))
                    
                print("""
                |======================================|
                |     Escolha o que deseja editar:     | 
                |======================================|
                |1 - Tipo                              |
                |2 - Nome                              |
                |3 - Idade                             |
                |4 - Todas as informações              |
                |======================================|
                """)
                opcao = int(input("Opção: "))
                    
                if opcao == 1:
                    novo_tipo = input("Novo tipo: ")
                    editar = f"update petshop set tipo_pet = '{novo_tipo}' where id = {pet_id}"
                elif opcao == 2:
                    novo_nome = int(input("Novo nome: "))
                    editar = f"update petshop set nome_pet = '{novo_nome}' where id = {pet_id}"
                elif opcao == 3:
                    nova_idade = input("Nova idade: ")
                    editar = f"update petshop set idade = '{nova_idade}' where id = {pet_id}"
                elif opcao == 4:
                    novo_tipo = input("Novo tipo:")
                    novo_nome = input("Novo nome:")
                    nova_idade = input("Nova idade:")
                    
                    editar = f"""
                        update petshop set tipo_pet = '{novo_tipo}', nome_pet = '{novo_nome}', idade = {nova_idade},
                        where id = {pet_id}
                    """    
                else:
                    print("Opção invalida.")
                    break
                
                inst_cadastro.execute(editar)
                conn.commit()
                print("Registro atualizado com sucesso!")
            except ValueError:
                print("Erro: Certifique-se de inserir valores validos.")

        case 4:
            try:
                print("""\n
                    |============================|       
                    |         EXCLUIR PET        |
                    |============================|
                    """)
                
                print("""
                |=====================================|
                |     Escolha o tipo de exclusão:     |
                |=====================================|
                |1 - Excluir um registro especifico   |
                |2 - Excluir todos os registros       |
                |=====================================|
                """)
                opcao = int(input("Opção: "))
                
                if opcao == 1:
                    pet_id = int(input("Digite o ID do pet para excluir: "))
                    exclusao = f"delete from petshop where id = {pet_id}"
                    inst_cadastro.execute(exclusao)
                    conn.commit()
                    print(f"Pet com ID {pet_id} excluído com sucesso!")
                    
                elif opcao == 2: 
                    inst_cadastro.execute("truncate table petshop") 
                    conn.commit()
                    print("Exclusão de todos os registros feito com sucesso.")
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Erro: Certifique-se de inserir valores válidos!")

    input("\nPressione qualquer tecla para continuar.")
