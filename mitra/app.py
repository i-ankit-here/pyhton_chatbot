# IMPORTING REQUIRED LIBRARIES AND MODULES
from flask import Flask, render_template, request, jsonify
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import string

#ACCESSING INFORMATION STORED IN JSON FILE
with open('intents.json', 'r', encoding="utf8") as file:
    intents_data = json.load(file)


#FUNCTIONS TO PROCESS VARIOUS TEXTS

def preprocess_text(text):
    # TOKENIZATION, LOWERCASING, REMOVING PUNCTUATION, REMOVING STOPWORDS, LEMMATIZATION
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(tokens)

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

#PREPARING INPUTS FOR PIPELINE
texts = [preprocess_text(process_content(intent) + intent['url']) for intent in intents_data['intents']]
labels = [intent["title"] for intent in intents_data['intents']]

#PREPARING PIPELINE FOR TRAINING
vectorizer = TfidfVectorizer()
classifier = SVC(kernel='linear')
pipeline = Pipeline([
    ('tfidf', vectorizer),
    ('clf', classifier)
])

#EXECUTING PIPELINE FOR INTENT PREDICTION
pipeline.fit(texts, labels)
def predict_intent(query):
    query_processed = preprocess_text(query)
    intent = pipeline.predict([query_processed])
    return intent[0]

#DEFINING DOMAINS AND SUBDOMAINS
About_NITJ=["Why NITJ","Reach Us","Institute Flyers","Organisational Chart","NITJ Rankings & Awards","Virtual Tour","Newsletters","General FAQs","Other"]
Administration=["NIT Council","Hostel Administration","Senate","Finance Committee","Building and Works Committee","System of Evaluation and Grant of Division","Other"]
Leadership=["Chairperson","Registrar","Administrative Officers","Board of Governors","Technical Officers","Other"]
Cells=["RTI Cell","Equal Opportunities and SC/ST/OBC/PwD Cell","Women Cell","Proctorial Cell","Student Grievances Cell","Public Grievances Cell","Staff Grievances Cell","Other"]
Departments=["Computer Science and Engineering","Information Technology","Instrumentation and Control Engineering","Industrial and Production Engineering","Electrical Engineering","Physics","Electronics and Communication Engineering","Civil Engineering","Chemical Engineering","Biotechnology","Chemistry","Humanities and Management","Mathematics and Computing","Mechanical Engineering","Textile Technology","Center for Energy and Environment","Other"]
Academics=["UMC Rules","Academic Circulars & Notices","Grade Calculation","Student Portal","Online Application for Verification of Degree","Results","CGPA Criteria and Medium of Education","Academic Section Officials","Other"]
Admissions=["Bachelor of Technology","Master of Technology","Master of Business Administration","Master of Science","Post Graduate Diploma","Doctor of Philosophy","International Students","Anti Ragging Cell","National anti-Ragging Programme","Other"]
Alumni=["Convocation","Past Convocations","Other"]
Life_at_NITJ=["Discover Student Life","Explore NITJ","Other"]
headers={'About NITJ':About_NITJ,'Administration':Administration,'Leadership':Leadership,'Cells':Cells,'Departments':Departments,'Academics':Academics,'Admissions':Admissions,'Alumni':Alumni,'Life at NITJ':Life_at_NITJ}

#FUNCTIONS TO PRODUCE BOT RESPONSE
def get_Chat_response(text1):
        if process_chat(text1)=="" or process_chat(text1) == "none":
            response=["For information about NITJ, please visit","<a href='https://www.nitj.ac.in'>https://www.nitj.ac.in</a>"]
            return response
        elif process_chat(text1)=="other":
            response=["Please specify"]
            return response
        else:
            key=''
            for i in headers.keys():
                if process_chat(text1)==process_chat(i):
                    key+=i
            if key:
                response = headers[key] 
                return response
            elif process_chat(text1)=="" or process_chat(text1)=="none":
                response=["For information about NITJ, please visit","<a href='https://www.nitj.ac.in'>https://www.nitj.ac.in</a>"]
            elif process_chat(text1)=="other":
                response=["Please specify"]
                return response
            else:
                intent = predict_intent(text1)
                if intent:
                    response = generate_response(intent)
                else:
                    response = "Sorry, I'm not sure how to help with that."
        if process_chat(text1)=='exit':
            pass
        return response

def generate_response(intent):
    for intent_data in intents_data['intents']:
        if intent_data['title'] == intent:
            content=process_content(intent_data)
            if content:
                return [content,"You can find information here:","<a href="+intent_data['url']+">"+intent_data['url']+"</a>"] 
            else:
                return ["You can find information here:","<a href="+intent_data['url']+">"+intent_data['url']+"</a>"] 
    return ["Sorry, I couldn't find information on that topic","You can try again by giving more specific keywords"]

def process_chat(s):
    s=s.lower().strip()
    return s

#SERVING BOT USING FLASK
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)

if __name__ == '__main__':
    app.run()
