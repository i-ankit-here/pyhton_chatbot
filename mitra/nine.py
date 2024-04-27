import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import string

with open('intents.json', 'r', encoding="utf8") as file:
    intents_data = json.load(file)

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Lowercasing
    tokens = [token.lower() for token in tokens]
    
    # Removing punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return " ".join(tokens)

# Preprocess intents
def process_str(s):
    tokens= word_tokenize(s)
    return " ".join(tokens)

def process_content(intent):
    content_string= ""
    for str in intent['content']:
        str=process_str(str)
        if not(str==''):
            content_string=content_string+'\n'+str+'\n'
    return content_string

texts = [preprocess_text(process_content(intent) + intent['url']) for intent in intents_data['intents']]
labels = [intent["title"] for intent in intents_data['intents']]

vectorizer = TfidfVectorizer()
classifier = SVC(kernel='linear')
pipeline = Pipeline([
    ('tfidf', vectorizer),
    ('clf', classifier)
])

pipeline.fit(texts, labels)

def predict_intent(query):
    query_processed = preprocess_text(query)
    intent = pipeline.predict([query_processed])
    return intent[0]

def generate_response(intent):
    for intent_data in intents_data['intents']:
        if intent_data['title'] == intent:
            content=process_content(intent_data)
            if content:
                return f"{content}"+'\n'+f"You can find information here: {intent_data['url']}"  
            else:
                print(f"You can find information here: {intent_data['url']}")
    return "Sorry, I couldn't find information on that topic."

def process_chat(s):
    s=s.lower().strip()
    return s


About_NITJ=["Why NITJ","Reach Us","Institute Flyers","Organisational Chart","NITJ Rankings & Awards","Virtual Tour","Newsletters","General FAQs"]
Administration=["NIT Council","Hostel Administration","Senate","Finance Committee","Building and Works Committee","System of Evaluation and Grant of Division"]
Leadership=["Chairperson","Registrar","Administrative Officers","Board of Governors","Technical Officers"]
Cells=["RTI Cell","Equal Opportunities and SC/ST/OBC/PwD Cell","Women Cell","Proctorial Cell","Student Grievances Cell","Public Grievances Cell","Staff Grievances Cell"]
Departments=["Computer Science and Engineering","Information Technology","Instrumentation and Control Engineering","Industrial and Production Engineering","Electrical Engineering","Physics","Electronics and Communication Engineering","Civil Engineering","Chemical Engineering","Biotechnology","Chemistry","Humanities and Management","Mathematics and Computing","Mechanical Engineering","Textile Technology","Center for Energy and Environment"]
Academics=["UMC Rules","Academic Circulars & Notices","Grade Calculation","Student Portal","Online Application for Verification of Degree","Results","CGPA Criteria and Medium of Education","Academic Section Officials",]
Admissions=["Bachelor of Technology","Master of Technology","Master of Business Administration","Master of Science","Post Graduate Diploma","Doctor of Philosophy","International Students","Anti Ragging Cell","National anti-Ragging Programme",]
Alumni=["Convocation","Past Convocations"]
Life_at_NITJ=["Discover Student Life","Explore NITJ"]
headers={'About NITJ':About_NITJ,'Administration':Administration,'Leadership':Leadership,'Cells':Cells,'Departments':Departments,'Academics':Academics,'Admissions':Admissions,'Alumni':Alumni,'Life at NITJ':Life_at_NITJ}

print("Bot: Hey there!")

while True:
    print("Bot: With which of the following can I help you?",end='\n\t~ ')
    for i in headers.keys():
        print(i,end=" ~ ")
    user=input('\nYou: ')
    if process_chat(user)=='exit':
        break
    elif process_chat(user)=="" or process_chat(user)=="none":
        print("Bot: For information about NITJ visit ~ https://www.nitj.ac.in")
    else:
        key=''
        for i in headers.keys():
            if process_chat(user)==process_chat(i):
                key+=i
        if key:
            print(f"Bot: Information about which of the following do you require from {key}?")
            # for j in headers[key]:
            #     print(j,end=" ~ ")
            print("\t",headers[key]) 
        else:
            print("Bot: Kindly choose from the fields specified for accurate information!")
            continue
        user=input('You: ')
        if process_chat(user)=='exit':
            break
        elif process_chat(user)=="" or process_chat(user)=="none":
            print("Bot: For information about NITJ visit ~ https://www.nitj.ac.in")
            continue
        else:
            intent = predict_intent(user)
            if intent:
                response = generate_response(intent)
            else:
                response = "Sorry, I'm not sure how to help with that."
            print("Bot:", response)
            print('\n\n')
    print('Bot: Do you want to continue?(yes/exit)')
    user=input('You: ')
    if process_chat(user)=='exit':
        break
    
    
            
        
        




# print("Bot: Hi there! How can I assist you today?")
# while True:
#     user_input = input("You: ")
#     intent = predict_intent(user_input)
#     if intent:
#         response = generate_response(intent)
#     else:
#         response = "Sorry, I'm not sure how to help with that."
#     print("Bot:", response)