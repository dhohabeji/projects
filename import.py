import requests
import json
import unicodedata

open_quizz_db_data = (
    ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050828847/OpenQuizzDB_050/openquizzdb_50.json"),
    ("Arts", "Musée du Louvre", "https://www.kiwime.com/oqdb/files/1086624389/OpenQuizzDB_086/openquizzdb_86.json"),
    ("Cinéma", "Alien", "https://www.kiwime.com/oqdb/files/3241454997/OpenQuizzDB_241/openquizzdb_241.json"),
    ("Cinéma", "Star wars", "https://www.kiwime.com/oqdb/files/1090993427/OpenQuizzDB_090/openquizzdb_90.json"),
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    out_questions_data = []
    try:
        response = requests.get(url)
    except:
        print("Exception pour la requete HTTP GET : " + url)
    else:
        try:
            data = json.loads(response.text)
            all_quizz = data["quizz"]["fr"]
            for quizz_title, quizz_data in all_quizz.items():
                out_filename = get_quizz_filename(categorie, titre, quizz_title)
                print(out_filename)
                out_questionnaire_data["difficulte"] = quizz_title
                for question in quizz_data:
                    question_dict = {}
                    question_dict["titre"] = question["question"]
                    question_dict["choix"] = []
                    for ch in question["propositions"]:
                        question_dict["choix"].append((ch, ch==question["réponse"]))
                    out_questions_data.append(question_dict)
                out_questionnaire_data["questions"] = out_questions_data
                out_json = json.dumps(out_questionnaire_data)

                file = open(out_filename, "w")
                file.write(out_json)
                file.close()
                print("end")
        except:
            print(f"Exception dans la désérialisation ou l'utilisation des données (questionnaire : {titre}, url: {url})")

    

for quizz_data in open_quizz_db_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])

