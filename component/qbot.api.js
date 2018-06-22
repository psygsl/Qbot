
function ask_qbot(api, param, callback, default_result) {
    var result = null;
    $.ajax({
        //       url:'/api/' + api + param,
//        url:'/api/' + api + param,
        url:'http://127.0.0.1:5001/'+api + param,
        type:'get',
        async: callback!=null,
        xhrFields: {
       withCredentials: true
    },
    crossDomain: true,
        success:function(response){
            result = response? response: default_result;
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert(XMLHttpRequest.status);
            //alert(XMLHttpRequest.readyState);
            //alert(textStatus);
            result = default_result;
        },
        complete: function(XMLHttpRequest, textStatus) {
            callback? callback(result):false;
        }
    });
    return result;
}

function kb_convo(kw, key, callback){
  var reply = {}
    reply[key] = {
        "says":
            [
                "Sorry, I don't get it, I may not yet have answer to your question 😕. Pls try re-phrase, maybe I can figure it out",
            ],
        "reply": [
            {
                "question": "Start Over",
                "answer": "ice"
            }
        ]
    };
    ask_qbot('v1.0/kb_convo','?q='+kw, callback, reply);
  //return reply;
}

function kb_convo_v2(kw, key, callback){
    var reply = {}
    reply[key] = {
        "says":
            [
                "Sorry, I don't get it, I may not yet have answer to your question 😕. Pls try re-phrase, maybe I can figure it out",
            ],
        "reply": [
            {
                "question": "Start Over",
                "answer": "ice"
            }
        ]
    };
    ask_qbot('v1.0/kb_convo2','?q='+kw, callback, {'convo': reply,'intent':'qna',});
    //return reply;
}

function stripe_kw(kw, callback) {
    reply = {'kw':kw, 'q':kw }
    ask_qbot('v1.0/get_kw','?kw='+kw, callback, reply);
}

function heartbeat(callback) {
    reply = {'stats':'heartbeat failure, possible connection lost' }
    ask_qbot('v1.0/get_session_stats','', callback, reply);
}