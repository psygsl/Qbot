from flask import Flask, jsonify, request, current_app, session
from functools import wraps
from dpm.predict import Prediction
import json
from ms_qna.webservice import QnAService
from flask_cors import CORS
from nlp import qbot_kw
import uuid
from pool.ai_pool import  AiPool
import time
from nlp.qbot_uii import QbotUII
from nlp.qbot_l2uii import QbotL2UII
from nlp.qbot_ner import QbotNER
import socket
from dbsvc.tasks import *
from session.MemSession import MemSession
import logging

# create console log stream
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log.log')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


# enable json support
def support_jsonp(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            res = f(*args,**kwargs)
            data = str(res.data)
            content = str(callback) + '(' + data + ')'
            return current_app.response_class(content, mimetype='application/javascript', status=res.status_code)
        else:
            return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
app.config.from_object('config')
uii = QbotUII(app.config)
l2uii = QbotL2UII(app.config)
memory = MemSession()

CORS(app, resources={r'/v1.0/*': {'origins':'*', 'supports_credentials':'true'}})
CORS(app, resources={r'/api/v1.0/*':{'origins':'*', 'supports_credentials':'true'}})

qnaService = QnAService(app.config['QNA_APP_ID'],app.config['QNA_APP_KEY'],app.config['QNA_APP_TOP'])
qippService = QnAService(app.config['QIPP_APP_ID'],app.config['QIPP_APP_KEY'],app.config['QNA_APP_TOP'])


@app.before_first_request
def initialize():
    pass


@app.before_request
def initialize_session():
    ip = request.remote_addr
    init_session_state(ip)


def init_session_state(ip):
    # store basic conversation information to session object
    # under control of flask
    if 'session_id' not in session: # set default session
        session['session_id'] = str(uuid.uuid4())
        InitSession.delay(session['session_id'], ip, HOST_NAME, HOST_IP)
    # initialize conversation state
    if 'intent' not in session:
        session['intent'] = ''
    if 'dialog_state' not in session:
        session['dialog_state'] = ''
    if 'stats' not in session:
        session['stats'] = ''

    # initialize session memory. to save conversation relevant parameter
    if session['session_id'] not in memory.Sessions():
        memory.InitSession(session['session_id'], ip)


@app.route('/')
def index():
    ip = request.remote_addr
    init_session_state(ip)

    return jsonify({'API server':'Qbot', 'client_ip': ip, 'session': session['session_id']})


@app.route('/v1.0/dpm', methods=['GET'])
def get_dpm():
    dpm = Prediction()
#    param = load('dpm.json')
    param = json.loads(request.args.get('str_param'))
    predict = dpm.get_predict(param)
    return jsonify({'predict': predict})


@app.route('/v1.0/kb_answer', methods=['GET', 'POST'])
def kb_answer():
    if request.method == 'POST':
        q = request.form['q']
    else:
        q = request.args.get('q')
    ans = qnaService.get_answer(q)
    return jsonify(ans)


@app.route('/v1.0/kb_convo', methods=['GET', 'POST'])
@support_jsonp
def kb_convo():
    if request.method == 'POST':
        q = request.form['q']
    else:
        q = request.args.get('q')

    ans = qnaService.get_convo(q)
    return jsonify(ans)


@app.route('/v1.0/kb_convo2', methods=['GET', 'POST'])
@support_jsonp
def kb_convo2():
    q, bTest = qbot_kw.formulate_query(request.form['q'] if request.method=='POST' else request.args.get('q'))

    session['stats'] = 'Looks it take me longer time than usual to find best answer. Still trying to be smart'
    aiPool = AiPool(app.config, HOST_NAME, HOST_IP, uii, l2uii, memory)
    start = time.time()
    ans = aiPool.run_query_ui(q, session['session_id'], bTest)
    end = time.time()
    session['stats'] = ''
    ModuleLatency.delay('KB_CONVO', end - start, HOST_NAME, HOST_IP)
    logger.debug('[KB_CONV] Query used time %f' % (end-start))
    UpdateSessionStatus.delay(session['session_id'],
                              {'intent': session['intent'],
                               'dialog_state': session['dialog_state'],
                               'ip':request.remote_addr},
                              HOST_NAME, HOST_IP)
    return jsonify(ans)


@app.route('/v1.0/qbot_uii', methods=['GET', 'POST'])
@support_jsonp
def get_qbot_uii():
    q = request.form['q'] if request.method == 'POST' else request.args.get('q')
    category = uii.getCategory(q, default='NA')
    l2category = l2uii.getCategory(q, default='NA')
    ner = QbotNER(app.config)
    outputs, ners, score = ner.getEntities(q)
    return jsonify({'L1': category, 'L2': l2category, 'NER': {'Sequence': outputs, 'Tag': ners, 'Score': float(score)}})


@app.route('/v1.0/get_session_stats', methods=['GET', 'POST'])
@support_jsonp
def get_session_stats():
    status = session['stats']
    return jsonify({'stats': status})


@app.route('/v1.0/active_session', methods=['GET', 'POST'])
@support_jsonp
def active_session():
    # not implemented
    return jsonify({})


@app.route('/v1.0/get_kw', methods=['GET', 'POST'])
def get_kw():
    q, _ = qbot_kw.formulate_query(request.form['kw'] if request.method == 'POST' else request.args.get('kw'))
    kw = qbot_kw.extract_kw(q)
    return jsonify({'kw':'na', 'q': 'na'}) if not kw else jsonify({'kw': kw, 'q': q})


@app.route('/v1.0/kb_download', methods=['GET'])
def kb_download():
    ans = qnaService.get_knowledgebase()
    return jsonify(ans)


@app.route('/v1.0/voice_text', methods=['GET','POST'])
@support_jsonp
def voice_text():
    req_file = request.files["file"]
    ans = qnaService.get_text(req_file)
    return jsonify(ans)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
