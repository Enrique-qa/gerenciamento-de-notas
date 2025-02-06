import streamlit as st
import pandas as pd
import sqlite3
from streamlit_router import StreamlitRouter

#credenciais
adminUser = "admin"
adminPassword = "admin"
studentUser = "user"
studentPassword = "user"

#dados originais
materias = { #dicionários de arrays
    "Cod": ["1", "2", "3", "4", "5"],
    "Matérias": ["Engenharia de Software I", "Estrutura de Dados II", "Gerência de Projetos", "Programação Orientada a Objetos", "Sistemas Operacionais"],
}
alunos = { #dicionários de arrays
    "Cod": ["1", "2", "3", "4", "5", "6", "7", "8"],
    "Alunos": ["Amanda", "Bruno", "Carlos", "Elias", "Enrique", "João", "Vitor", "Xenosvaldo"]
}

#banco de dados sqlite
def init_db():
    conn = sqlite3.connect('notas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY,
            nome TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY,
            nome TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            aluno_id INTEGER,
            materia_id INTEGER,
            bimestre1 REAL,
            bimestre2 REAL,
            PRIMARY KEY (aluno_id, materia_id),
            FOREIGN KEY (aluno_id) REFERENCES alunos(id),
            FOREIGN KEY (materia_id) REFERENCES materias(id)
        )
    ''') 

    #inserindo os dados originais das materias no banco de dados
    for idx, materia in enumerate(materias["Matérias"]):
        cursor.execute('''
            INSERT OR IGNORE INTO materias (id, nome) VALUES (?, ?)
        ''', (materias["Cod"][idx], materia))

    #inserindo os dados originais dos alunos no banco de dados
    for idx, aluno in enumerate(alunos["Alunos"]):
        cursor.execute('''
            INSERT OR IGNORE INTO alunos (id, nome) VALUES (?, ?)
        ''', (alunos["Cod"][idx], aluno))

    conn.commit()
    conn.close()

#carregando dados do banco de dados
def load_data():
    conn = sqlite3.connect('notas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    conn.close()

    #convertendo os dados para dataframe
    mat = pd.DataFrame(materias, columns=["ID", "Matérias"])
    al = pd.DataFrame(alunos, columns=["ID", "Alunos"])

    return mat, al

###########################paginas###########################
#pagina de login
def login():
    #importando as imagens pelo nome
    imagem_esquerda = "unifimes.png"
    imagem_direita = "sistemas.png"

    #usando colunas para posicionar as imagens
    col1, col2 = st.columns(2)

    with col1:
        #exibir a imagem da esquerda
        st.image(imagem_esquerda, width=85)
        
    with col2:
        #exibir a imagem da direita
        st.image(imagem_direita, width=100)
        
    #botões para redirecionar   
    col1, col2 = st.columns(2)
    
    with col1:    
        if st.button("Ir para a Unifimes", key="button_esquerda"):
                st.markdown('<meta http-equiv="refresh" content="0; url=https://unifimes.edu.br/" />', unsafe_allow_html=True)

    with col2:
        if st.button("Ir para Sistemas", key="button_direita"):
                st.markdown('<meta http-equiv="refresh" content="0; url=https://unifimes.edu.br/avada_portfolio/sistemas-de-informacao/" />', unsafe_allow_html=True)
    st.divider()

    #titulo
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Sistema de Notas</h1>", unsafe_allow_html=True)
    st.subheader("Faça seu login")
    st.divider()

    #inputs de usuario e senha
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")

    #validação de usuario
    if st.button("Login", key="login_button"):
        if (username == adminUser and password == adminPassword) or (username == studentUser and password == studentPassword):
            st.success("Login bem-sucedido!")
            if username == adminUser:
                router.redirect("/admin") #redirecionamento para pagina admin
            else:
                router.redirect("/student") #redirecionamento para pagina estudante
        else:
            st.error("Usuário ou senha inválidos. Tente novamente.")

#pagina de aministrador
def admin():
    if st.button("Sair", key="exit"):
        router.redirect("/")

    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Bem-vindo: Administrador!</h1>", unsafe_allow_html=True)
    st.divider()
    st.write("Selecione a opção desejada:")
    if st.button("Inserir Notas", use_container_width=True):
        router.redirect("/newnote")

    if st.button("Editar Notas", use_container_width=True):
        router.redirect("/editnote")
    
    if st.button("Visualizar Notas", use_container_width=True):
        router.redirect("/viewnote")

#pagina de cadastro de notas
def newnote():
    if st.button("Voltar"):
        router.redirect("/admin")

    mat, al = load_data()

    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Cadastro de Notas</h1>", unsafe_allow_html=True)
    st.divider()

    st.subheader("Selecione uma Matéria")

    selected_materias = []
    for row in mat.itertuples():
        col1, col2 = st.columns([8, 2])
        with col1:
            st.markdown(f"<p style='margin: 0;'>{row.Matérias}</p>", unsafe_allow_html=True)
        with col2:
            selected = st.checkbox("", key=f"materia_{row.ID}")
            if selected:
                selected_materias.append(row)

    st.divider()

    if selected_materias:
        st.subheader("Selecione Alunos")
        selected_alunos = []
        for row in al.itertuples():
            col1, col2 = st.columns([8, 2])
            with col1:
                st.markdown(f"<p style='margin: 0;'>{row.Alunos}</p>", unsafe_allow_html=True)
            with col2:
                selected = st.checkbox("", key=f"aluno_{row.ID}")
                if selected:
                    selected_alunos.append(row)

        st.divider()

        if selected_alunos:
            st.subheader("Digite as Notas")
            notas = []
            for aluno in selected_alunos:
                for materia in selected_materias:
                    col1, col2 = st.columns([5, 5])
                    with col1:
                        nota_b1 = st.number_input(
                            f"1-Bimestre",
                            min_value=0.0,
                            max_value=10.0,
                            key=f"nota_{aluno.ID}_{materia.ID}_b1",
                        )
                    with col2:
                        nota_b2 = st.number_input(
                            f"2-Bimestre",
                            min_value=0.0,
                            max_value=10.0,
                            key=f"nota_{aluno.ID}_{materia.ID}_b2",
                        )
                    notas.append((aluno.ID, materia.ID, nota_b1, nota_b2))

            if st.button("Salvar Notas"):
                conn = sqlite3.connect("notas.db")
                cursor = conn.cursor()

                for aluno_id, materia_id, b1, b2 in notas:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO notas (aluno_id, materia_id, bimestre1, bimestre2) 
                        VALUES (?, ?, ?, ?)
                        """,
                        (aluno_id, materia_id, b1, b2),
                    )

                conn.commit()
                conn.close()
                st.success("Notas salvas com sucesso!")

                # Exibir tabela com as notas
                notas_display = []
                for aluno in selected_alunos:
                    for materia in selected_materias:
                        for aluno_id, materia_id, b1, b2 in notas:
                            if aluno_id == aluno.ID and materia_id == materia.ID:
                                media = (b1 + b2) / 2
                                status = "Aprovado" if media >= 6 else "Reprovado"
                                notas_display.append([aluno.Alunos, materia.Matérias, b1, b2, media, status])

                if notas_display:
                    df_notas = pd.DataFrame(notas_display, columns=["Aluno", "Matéria", "Nota 1º Bimestre", "Nota 2º Bimestre", "Média", "Status"])
                    st.write(df_notas)

#pagina de edição de notas
def editnote():
    if st.button("Voltar"):
        router.redirect("/admin")

    mat, al = load_data()

    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Edição de Notas</h1>", unsafe_allow_html=True)
    st.divider()

    st.subheader("Selecione uma Matéria")

    selected_materias = []
    for row in mat.itertuples():
        col1, col2 = st.columns([8, 2])
        with col1:
            st.markdown(f"<p style='margin: 0;'>{row.Matérias}</p>", unsafe_allow_html=True)
        with col2:
            selected = st.checkbox("", key=f"materia_{row.ID}")
            if selected:
                selected_materias.append(row)

    st.divider()

    if selected_materias:
        st.subheader("Selecione Alunos")
        selected_alunos = []
        for row in al.itertuples():
            col1, col2 = st.columns([8, 2])
            with col1:
                st.markdown(f"<p style='margin: 0;'>{row.Alunos}</p>", unsafe_allow_html=True)
            with col2:
                selected = st.checkbox("", key=f"aluno_{row.ID}")
                if selected:
                    selected_alunos.append(row)

        st.divider()

        if selected_alunos:
            st.subheader("Edite as Notas")
            notas = []
            for aluno in selected_alunos:
                for materia in selected_materias:
                    conn = sqlite3.connect("notas.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT bimestre1, bimestre2 FROM notas 
                        WHERE aluno_id = ? AND materia_id = ?
                        """,
                        (aluno.ID, materia.ID),
                    )
                    result = cursor.fetchone()
                    conn.close()

                    nota_b1 = result[0] if result else 0.0
                    nota_b2 = result[1] if result else 0.0

                    col1, col2 = st.columns([5, 5])
                    with col1:
                        nota_b1 = st.number_input(
                            f"1-Bimestre",
                            min_value=0.0,
                            max_value=10.0,
                            value=nota_b1,
                            key=f"nota_{aluno.ID}_{materia.ID}_b1",
                        )
                    with col2:
                        nota_b2 = st.number_input(
                            f"2-Bimestre",
                            min_value=0.0,
                            max_value=10.0,
                            value=nota_b2,
                            key=f"nota_{aluno.ID}_{materia.ID}_b2",
                        )
                    notas.append((aluno.ID, materia.ID, nota_b1, nota_b2))

            if st.button("Salvar Notas"):
                conn = sqlite3.connect("notas.db")
                cursor = conn.cursor()

                for aluno_id, materia_id, b1, b2 in notas:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO notas (aluno_id, materia_id, bimestre1, bimestre2) 
                        VALUES (?, ?, ?, ?)
                        """,
                        (aluno_id, materia_id, b1, b2),
                    )

                conn.commit()
                conn.close()
                st.success("Notas atualizadas com sucesso!")

                # Exibir tabela com as notas
                st.subheader("Notas dos Alunos")
                notas_display = []
                for aluno in selected_alunos:
                    for materia in selected_materias:
                        for aluno_id, materia_id, b1, b2 in notas:
                            if aluno_id == aluno.ID and materia_id == materia.ID:
                                media = (b1 + b2) / 2
                                status = "Aprovado" if media >= 6 else "Reprovado"
                                notas_display.append([aluno.Alunos, materia.Matérias, b1, b2, media, status])

                if notas_display:
                    df_notas = pd.DataFrame(notas_display, columns=["Aluno", "Matéria", "Nota 1º Bimestre", "Nota 2º Bimestre", "Média", "Status"])
                    st.write(df_notas)

#pagina de visualização de notas
def viewnote():
    if st.button("Voltar"):
        router.redirect("/admin")

    mat, al = load_data()

    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Visualizar Notas</h1>", unsafe_allow_html=True)
    st.divider()

    st.subheader("Selecione as Matérias")
    selected_materias = []
    for idx, row in mat.iterrows():
        selected = st.checkbox(row["Matérias"], key=f"materia_{idx}")
        if selected:
            selected_materias.append(row)

    st.divider()

    if selected_materias:
        st.subheader("Notas dos Alunos")

        notas = []
        for materia in selected_materias:
            materia_id = materia["ID"]
            materia_nome = materia["Matérias"]

            conn = sqlite3.connect('notas.db')
            cursor = conn.cursor()

            cursor.execute("""
                SELECT alunos.nome, notas.bimestre1, notas.bimestre2
                FROM notas
                JOIN alunos ON alunos.id = notas.aluno_id
                WHERE notas.materia_id = ?
            """, (materia_id,))
            resultados = cursor.fetchall()
            conn.close()

            for aluno_nome, nota_b1, nota_b2 in resultados:
                media = (nota_b1 + nota_b2) / 2
                status = "Aprovado" if media >= 6 else "Reprovado"
                notas.append([aluno_nome, materia_nome, nota_b1, nota_b2, media, status])

        if notas:
            df_notas = pd.DataFrame(notas, columns=["Aluno", "Matéria", "Nota 1º Bimestre", "Nota 2º Bimestre", "Média", "Status"])
            st.write(df_notas)
        else:
            st.write("Nenhuma nota encontrada para as matérias selecionadas.")
    else:
        st.write("Selecione ao menos uma matéria para visualizar as notas.")

#pagina de estudante
# Página de estudante
def student():
    if st.button("Sair"):
        router.redirect("/")
        
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Notas do Aluno: Enrique</h1>", unsafe_allow_html=True)
    st.divider()

    conn = sqlite3.connect('notas.db')
    cursor = conn.cursor()

    # Consultar as notas do aluno Enrique
    cursor.execute("""
        SELECT materias.nome, notas.bimestre1, notas.bimestre2
        FROM notas
        JOIN alunos ON alunos.id = notas.aluno_id
        JOIN materias ON materias.id = notas.materia_id
        WHERE alunos.nome = ?
    """, ("Enrique",))
    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        notas = []
        for materia, nota_b1, nota_b2 in resultados:
            media = (nota_b1 + nota_b2) / 2
            status = "Aprovado" if media >= 6 else "Reprovado"
            notas.append([materia, nota_b1, nota_b2, media, status])

        df_notas = pd.DataFrame(notas, columns=["Matéria", "Nota 1º Bimestre", "Nota 2º Bimestre", "Média", "Status"])
        st.write(df_notas)
    else:
        st.write("Nenhuma nota encontrada para o aluno Enrique.")

# inicialização do banco de dados
init_db()   

# configuração do roteador
router = StreamlitRouter()
router.register(login, "/", methods=['GET'])
router.register(admin, "/admin", methods=['GET'])
router.register(newnote, "/newnote", methods=['GET'])
router.register(editnote, "/editnote", methods=['GET'])
router.register(student, "/student", methods=['GET'])
router.register(viewnote, "/viewnote", methods=['GET'])
router.serve()  