import threading
import time
from random import Random
from ai_wrapper import  lex_wrapper
from ms_qna.webservice import QnAService
from dbsvc.tasks import *
from nlp.qbot_uii import QbotUII
from ai_wrapper.qbot_stats import QbotStats
from ai_wrapper.delve_search import delve_search
from nlp.qbot_ner import QbotNER
from metric_stats.cockpit_crawler import get_cockpit
from flask import session
import logging

# create console log stream
logger = logging.getLogger()

class AiPool():
    def __init__(self, param, host_name, host_ip, uii, l2uii, memory):
        self.r = Random(time.time())
        self.qnaService = QnAService(param['QNA_APP_ID'], param['QNA_APP_KEY'], param['QNA_APP_TOP'])
        self.qippService = QnAService(param['QIPP_APP_ID'], param['QIPP_APP_KEY'], param['QNA_APP_TOP'])
        self.stats = 0
        self.answer = None
        self.lock = threading.Lock()
        self.lockAns = threading.Lock()
        self.HOST_NAME = host_name
        self.HOST_IP = host_ip
        self.uii = uii
        self.l2uii = l2uii
        self.config = param
        self.memory = memory
        #self.log_db = log_db

    def update_ans(self, ans, worker, state):
        self.lockAns.acquire()
        if self.answer is None:
            self.answer = {'intent': worker, 'dialogState': state, 'convo': ans }
            #self.stats += 1
            logger.debug(ans)
        elif ans['score'] > self.answer['convo']['score']:
            self.answer = {'intent': worker, 'dialogState': state, 'convo': ans }
            #self.stats += 1
            logger.debug(ans)
        else:
            pass
        self.lockAns.release()

    def update_status(self, inc):
        self.lock.acquire()
        self.stats += inc
        self.lock.release()

    def acquire_status(self):
        return self.stats

    def lex_query(self, q, session_id, bTest):
        start = time.time()
        ans = lex_wrapper.get_convo(q, session)
        logger.debug('lex call success')
        end = time.time()
        usedtime = end - start
        self.log_qna('Lex', bTest, ans['score'], q, ans, usedtime, session_id, 'dialog', ans['dialogState'])
        self.update_ans(ans, 'dialog', ans['dialogState'])
        self.update_status(1.6)

    def qna_query(self, q, session_id, bTest):
        start = time.time()
        ans = self.qnaService.get_convo(q)
        logger.debug('qna call success')
        end = time.time()
        usedtime = end - start
        self.log_qna('QnA', bTest, ans['score'], q, ans, usedtime, session_id, 'qna', 'Fullfilled')
        self.update_ans(ans, 'qna', 'Fulfilled')
        self.update_status(1)

    def run_query(self, q, session_id, bTest = False):
        worker_list = [threading.Thread(target=self.qna_query, args=[q, session_id, bTest]),
                       threading.Thread(target=self.lex_query, args=[q, session_id, bTest])]
        for worker in worker_list:
            worker.start()
        while True:
            #wait query any thread complete
            if self.acquire_status() == 0:
                # in case no response at all will wait until any thread timeout occur
                continue
            elif self.acquire_status() < 2:
                self.update_status(1/100)
            else:
                return  self.answer
            time.sleep(0.2)

    def log_qna(self, source, isTest, score, question, answer, latency, session_id, intent, state):
        LogActivity.delay(target='conversation', activity={'HOST_NAME':self.HOST_NAME, 'HOST_IP': self.HOST_IP,
                                                           'Test': isTest,
                                                           'SessionID': session_id,
                                                           'Source': source, 'Client': question,
                                                           'Reply': answer, 'Latency': latency, 'Score': score,
                                                           'Intent':intent, 'State': state})

    def log_module_latency(self, module, latency):
        ModuleLatency.delay(module, latency, self.HOST_NAME, self.HOST_IP)

    def log_text_classification(self, module, text, category, latency, feedback):
        LogActivity.delay(target='text_classification', activity={'HOST_NAME': self.HOST_NAME,
                                                                  'HOST_IP': self.HOST_IP,
                                                                  'Module': module,
                                                                  'Text': text, 'Category': category,
                                                                  'Feedback': feedback,
                                                                  'Latency': latency})

    def qbot_stats_query_w_score(self, q, session_id, btest, source):
        start = time.time()
        stats = QbotStats(self.config, self.l2uii)
        ans = stats.get_convo(q, session_id)
        end = time.time()
        usedtime = end - start

        self.update_ans(ans, stats.Sub_Cat(), 'Fullfilled')
        self.log_module_latency(source, usedtime)
        return ans['score']

    def delve_query_w_score(self, q, session_id, btest, source):
        start = time.time()
        delve = delve_search()
        ner = QbotNER(self.config)
        outputs, ners, score = ner.getEntities(q)
        ans = delve.get_convo(q, ners)
        end = time.time()
        usedtime = end - start
        self.log_qna(source, btest, ans['score'], q, ans, usedtime, session_id, 'delv', 'Fullfilled')
        self.update_ans(ans, 'delv', 'Fullfilled')
        self.log_module_latency(source, usedtime)
        return ans['score']

    def qna_query_w_score(self, q, session_id, btest, source):
        start = time.time()
        if source == 'QIPP':
            ans = self.qippService.get_convo(q, strip_question=':')
        else:
            ans = self.qnaService.get_convo(q)
        end = time.time()
        usedtime = end - start

        self.log_qna(source, btest, ans['score'], q, ans, usedtime, session_id, 'qna', 'Fullfilled')
        self.update_ans(ans, 'qna', 'Fullfilled')
        self.log_module_latency(source, usedtime)
        return ans['score']

    def lex_query_w_score(self, q, session_id, btest):
        start = time.time()
        ans = lex_wrapper.get_convo(q, session_id)
        end = time.time()
        usedtime = end - start

        self.log_qna('Lex', btest, ans['score'], q, ans, usedtime, session_id, 'dialog', ans['dialogState'])
        self.update_ans(ans, 'dialog', ans['dialogState'])
        self.log_module_latency('Lex', usedtime)
        return ans['score']

    def cockpit_query_w_score(self, q, session_id, btest, source):
        start = time.time()
        # ner = QbotNER(self.config)
        # outputs, ners, score = ner.getEntities(q)

        ans = get_cockpit(q, self.l2uii)
        end = time.time()
        usedtime = end - start
        self.log_qna(source, btest, ans['score'], q, ans, usedtime, session_id, 'delv', 'Fullfilled')
        self.update_ans(ans, 'cockpit', 'Fullfilled')
        self.log_module_latency(source, usedtime)
        return ans['score']

    def run_task(self, task, *args, **kwargs):
        timeout = 2*60
        future = task.apply_async(args, kwargs)
        time_end = time.time() + timeout
        while True:
            try:
                return future.get(timeout = timeout)
            except TimeoutError:
                if time.time() < time_end:
                    continue
                raise

    def run_query_ui(self, q, session_id, bTest = False):
        if 'quit' in q:
            session['intent'] = 'QnA'

        ner = QbotNER(self.config)
        outputs, ners, score = ner.getEntities(q)
        # Pre-processing Module. pre-processing will change tags like metric type, date, person name to tags.  e.g. 2018-6 -> {DATE}, Maneesh Kumar
        #--> {PEOPLE},  5G Head -> {TITLE}.  NCDR -> {METRIC} .  MN MANO -> {DU}.  Mobile Network -> {BG}
        # output: after pre-processing, original quesiton together with taggee quesiton will be delivered to User Intention Module
        # output: another output of this pre-processing is parameter dictionary. this dictionary is global per session. it is like a memory
        # we will remember the input from that session

        # User Intention Module:  by this time this UII will not be troubled by various filters
        # this piece of code is not needed anymore. because global session parameter dictionary can store everything and
        # be used in different module queries
        if session['intent'] == 'dialog' and session['dialog_state'] not in ['Fulfilled', 'ElicitIntent']:
            category = 'Metric'
        elif session['intent'] == 'cockpit' and session['dialog_state'] not in ['Fulfilled', 'ElicitIntent']:
            category = 'Cockpit'
        else:
            start = time.time()
            category = self.uii.getCategory(q)
            end = time.time()
            logger.debug('[AI_POOL] %s' % category)
            self.log_module_latency('UII_CLASSIFY', end - start)

        # can we evaluate the likelihood of answer score.
        if category in ["QnA","QIPP"]:
            score = self.qna_query_w_score(q, session_id, bTest, category)
            if score <= 40:
                self.log_text_classification('UII', q, category, 0, 'NOK')
                self.lex_query_w_score(q, session_id, bTest)
            else:
                self.log_text_classification('UII', q, category, 0, 'SEEMS_OK')
        elif category in ['Qbot']:
            score = self.qbot_stats_query_w_score(q, session_id, bTest, category)
            if score <= 40:
                self.log_text_classification('UII', q, category, 0, 'NOK')
                self.qna_query_w_score(q, session_id, bTest, 'QnA')
            else:
                self.log_text_classification('UII', q, category, 0, 'SEEMS_OK')
        elif category in ['DELV']:
            score = self.delve_query_w_score(q, session_id, bTest, category)
            if score <= 40:
                self.log_text_classification('UII', q, category, 0, 'NOK')
                self.qna_query_w_score(q, session_id, bTest, 'QnA')
            else:
                self.log_text_classification('UII', q, category, 0, 'SEEMS_OK')
        elif category in ['Cockpit']:
            score = self.cockpit_query_w_score(q, session_id, bTest, category)
            if score <= 40:
                self.log_text_classification('UII', q, category, 0, 'NOK')
                self.qna_query_w_score(q, session_id, bTest, 'QnA')
            else:
                self.log_text_classification('UII', q, category, 0, 'SEEMS_OK')
        else:
            score = self.lex_query_w_score(q, session_id, bTest)
            if score <= 40:
                self.log_text_classification('UII', q, category, 0, 'NOK')
                self.qna_query_w_score(q, session_id, bTest, 'QnA')  # default call QnA KB
            else:
                self.log_text_classification('UII', q, category, 0, 'SEEMS_OK')

        session['intent'] = self.answer['intent']
        session['dialog_state'] = self.answer['dialogState']
        return self.answer
