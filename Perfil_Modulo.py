import instaloader, time, datetime, csv, re
import datetime, Subtarefas_Modulo

# Função que busca se os comentários do post analisado contém alguma das palavras-chaves relacionadas ao covid
def comentario_relacionado(comments):
    corona_list = ["coron", "covid", "quarentena", "homeoffice", "pandemia"]
    for comment in comments:
        for x in corona_list:
            string = comment.text.replace(" ", "")
            if Subtarefas_Modulo.kmp(string,x) != []:
                return True
    return False

# Função que busca se o texto do post analisado contém alguma das palavras-chaves relacionadas ao covid
def texto_relacionado(caption):
    corona_list = ["coron", "covid", "quarent", "homeoffice", "pand", "virus"]
    for x in corona_list:
        string = caption.replace(" ", "")
        if Subtarefas_Modulo.kmp(string,x) != []:
            return True
    return False

# Função que filtra se o post coletado tem relacionamento com o tema emprego
def emprego_relacionado(comments, caption):
    emprego_list = ['empreg', 'demiss', 'demit', 'homeoffice', 'trabalh', 'auxilio', 'auxílio']
    for x in emprego_list:
        string = caption.replace(" ", "")
        if Subtarefas_Modulo.kmp(string,x) != []:
            return True
    for comment in comments:
        for x in emprego_list:
            string = comment.text.replace(" ", "")
            if Subtarefas_Modulo.kmp(string,x) != []:
                return True
    return False


def coleta_perfil(loader):

    #filtra os emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                            "]+", flags=re.UNICODE)

    business_csv = str(input("Digite o nome do arquivo CSV que deve ser lido: ")) #decide o arquivo csv a ser lido
    cont = 0
    cont_max = int(input("Digite o número de posts que devem ser coletados do perfil: "))

    with open(business_csv+'.csv', 'r') as arquivo_csv:
        leitor = csv.reader(arquivo_csv, delimiter=',')
        for linha in leitor:
            username = linha[0]
            profile = instaloader.Profile.from_username(loader.context, username)
            print("-----NOVO PERFIL-----")
            print(profile.username)
            posts = profile.get_posts()
            with open(str(profile.username)+'.csv', 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Usuario", "Genero", "Data", "Likes", "Comentarios", "Texto", "Hashtags", "Patrocinado", "Usuarios marcados", "Comentário Rel.", "Texto Rel.", "PostId"])
                for post in posts:
                    comentarios = post.get_comments()
                    if post.is_video == False and post.caption != None and emprego_relacionado(comentarios, post.caption):
                        print(post.date)
                        cont += 1
                        print("Número de posts coletados: ", cont)
                        nome = post.owner_profile.full_name
                        if nome:
                            nome = nome.split()
                            genero = Subtarefas_Modulo.consulta_genero(nome[0])
                        else:
                            genero = "None"
                        writer.writerow([post.owner_username, genero, post.date, post.likes, post.comments,emoji_pattern.sub(r'', post.caption), post.caption_hashtags, post.is_sponsored, post.tagged_users, comentario_relacionado(comentarios), texto_relacionado(post.caption), post.shortcode]) #Coleta os dados referentes as colunas do arquivo csv
                    if cont == cont_max: #Caso o número necessário de posts seja coletado ou não exista mais posts nessa margem de tempo, finaliza o programa
                        print("Finalizado!!")
                        break