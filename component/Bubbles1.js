// core function

var _convo = {}
var more_count = 0;
var reply_count = 0;
var more_reply = 0;
function Bubbles(container, self, options) {
  // options
  options = typeof options !== "undefined" ? options : {}
  animationTime = options.animationTime || 60 // how long it takes to animate chat bubble, also set in CSS
  typeSpeed = options.typeSpeed || 1 // delay per character, to simulate the machine "typing"
  widerBy = options.widerBy || 2 // add a little extra width to bubbles to make sure they don't break
  sidePadding = options.sidePadding || 6 // padding on both sides of chat bubbles
  inputCallbackFn = options.inputCallbackFn || false // should we display an input field?

  var standingAnswer = "ice" // remember where to restart convo if interrupted

   // local memory for conversation JSON object
  var match_key = '';
  var match_cate = '';
  var response_count = 0;
  //--> NOTE that this object is only assigned once, per session and does not change for this
  // 		constructor name during open session.
  // set up the stage
  container.classList.add("bubble-container")
  var bubbleWrap = document.createElement("div")
  bubbleWrap.className = "bubble-wrap"
  container.appendChild(bubbleWrap)

  // this.tryTalk = function(here){
  //     (_convo[here] ? (standingAnswer = here): false) ?  this.reply(_convo[here]):false
  // }
  // install user input textfield
  this.typeInput = function(callbackFn) {
    var inputWrap = document.createElement("div")
    inputWrap.className = "input-wrap"
    var inputText = document.createElement("textarea")
    inputText.setAttribute("placeholder", "Ask me about Nokia Quality...")
    inputWrap.appendChild(inputText)
    inputText.addEventListener("keypress", function(e) {
      // register user input
      if (e.keyCode == 13) {
        e.preventDefault()
        typeof bubbleQueue !== false ? clearTimeout(bubbleQueue) : false // allow user to interrupt the bot
        var lastBubble = document.querySelectorAll(".bubble.say")    /*  Chris */
        lastBubble = lastBubble[lastBubble.length - 1]
        lastBubble.classList.contains("reply") &&
        !lastBubble.classList.contains("reply-freeform")
          ? lastBubble.remove()
          : false
        addBubble(
          '<span class="bubble-button bubble-pick" data-reply='+reply_count+'>' + this.value + "</span>",
          undefined,
          function() {},
          "reply reply-freeform",
          ''
        )
        more_reply = reply_count;
        reply_count += 1 ; 
        // callback
        typeof callbackFn === "function"
          ? callbackFn({
              input: this.value,
              convo: _convo,
              standingAnswer: standingAnswer,
              match_key:match_key,
              match_cate:match_cate
            })
          : false
         // this.tryTalk(this.value)
        this.value = ""
      }
    })
    container.appendChild(inputWrap)
    //bubbleWrap.style.paddingBottom = "100px"
    inputText.focus()
  }
  
  inputCallbackFn ? this.typeInput(inputCallbackFn) : false

    
  // init typing bubble
  var bubbleTyping = document.createElement("div")
  bubbleTyping.className = "bubble-typing imagine"
  for (dots = 0; dots < 3; dots++) {
    var dot = document.createElement("div")
    dot.className = "dot_" + dots + " dot"
    bubbleTyping.appendChild(dot)
  }
  bubbleWrap.appendChild(bubbleTyping)

  // accept JSON & create bubbles
  this.talk = function(convo, category, here ,dialogState) {
    // all further .talk() calls will append the conversation with additional blocks defined in convo parameter
    _convo = Object.assign(_convo, convo) // POLYFILL REQUIRED FOR OLDER BROWSER
    _convo['category'] = category;
    match_key = dialogState;
    match_cate = category;
    more_count = 0;
    this.reply(_convo[here],category,dialogState)
    here ? (standingAnswer = here) : false
  }
  this.charting = function(convo, category, here, intent) {
    more_count = 0;
    _convo = Object.assign(_convo, convo);
    _convo['category'] = category;    
    match_key = intent;
    match_cate = category;
    this.paint(_convo[here],category,intent);
    here ? (standingAnswer = here) : false
  }

  this.dialog = function(convo, here , dialogState){
    more_count = 0;
    this.reply(convo[here],dialogState)
    standingAnswer = false
  }

  this.reply = function(turn, category, dialogState) {
    turn = typeof turn !== "undefined" ? turn : _convo.ice
    questionsHTML = ""
    if (turn.reply !== undefined) {
    //      turn.reply.reverse()
      turn_reply_length = 0
      for (var i = 0; i < (turn.reply.length < 2 ? turn.reply.length : 2); i++) {
          ;(function(el, count) {
          turn_reply_length += 1
          questionsHTML +=
              '<span class="bubble-button" data-reply='+reply_count+' style="animation-delay: ' +
              animationTime / 2 * count +
              'ms" onClick="' +
              self +
              ".answer('" +
              el.answer +
              "');this.classList.add('bubble-pick')\">" +
              el.question +
              "</span>"
          })(turn.reply[i], i)
      }
      if(turn != undefined && turn['reply'].length>=2){
        questionsHTML += '<p class="delve_moreResult_show" data-more="'+more_reply+'">More</p>';
      }
      // for (var i = turn_reply_length; i < turn.reply.length; i++) {
      //     ;(function(el, count) {
      //     questionsHTML +=
      //         '<span class="bubble-button" data-reply='+reply_count+' style="display:none; animation-delay: ' +
      //         animationTime / 2 * count +
      //         'ms" onClick="' +
      //         self +
      //         ".answer('" +
      //         el.answer +
      //         "');this.classList.add('bubble-pick')\">" +
      //         el.question +
      //         "</span>"
      //     })(turn.reply[i], i)
      // }
    }
    orderBubbles(turn.says, category, dialogState, function() {
      bubbleTyping.classList.remove("imagine")
      questionsHTML !== ""
        ? addBubble(questionsHTML, category, function() {}, "reply", dialogState)
        : bubbleTyping.classList.add("imagine")
    })
  }

  this.paint = function(turn, category ,intent) {
    turn = typeof turn !== "undefined" ? turn : _convo.ice
    questionsHTML = ""
    if (turn.reply !== undefined) {
      turn.reply.reverse()
      for (var i = 0; i < turn.reply.length; i++) {
        ;(function(el, count) {
          questionsHTML +=
            '<span class="bubble-button" style="animation-delay: ' +
            animationTime / 2 * count +
            'ms" onClick="' +
            self +
            ".answer('" +
            el.answer +
            "');this.classList.add('bubble-pick')\">" +
            el.question +
            "</span>"
        })(turn.reply[i], i)
      }
    }
    addBubble(turn.says, category, function() {}, '' ,intent)
  }
  // navigate "answers"
  this.answer = function(key) {
    more_reply +=1;
    reply_count += 1;
    more_count = 0;
    var func = function(key) {
      typeof window[key] === "function" ? window[key]() : false
    }
    dialogState_data = ''
    if(_convo[key]['reply'][0]['answer']!='ice'){
      dialogState_data = 'Fullfilled'
    }
    _convo[key] !== undefined
      ? (this.reply(_convo[key],_convo['category'],dialogState_data), (standingAnswer = key))
      : func(key)
  }

  // api for typing bubble
  this.think = function() {
    bubbleTyping.classList.remove("imagine")
    this.stop = function() {
      bubbleTyping.classList.add("imagine")
    }
  }

  // "type" each message within the group
  var orderBubbles = function(q, category, dialogState, callback) {
    var start = function() {
      setTimeout(function() {
        callback()
      }, animationTime)
    }
    var position = 0
    for (var nextCallback = position + q.length - 1;nextCallback >= position;nextCallback--) {
      (function(callback, index) {
        start = function() {
          addBubble(q[index], category, callback, '', dialogState)
        }
      })(start, nextCallback)
    }
    start()
  }

  
  // create a bubble
  var bubbleQueue = false
  var addBubble = function(say, category, posted, reply, dialogState) {
    
    reply = typeof reply !== "undefined" ? reply : ""
    // create bubble element
    var bubble = document.createElement("div")
    if(dialogState=='ElicitSlot'){
      bubble.className = "bubble imagine ElicitSlot " + reply
    }
    else{
      bubble.className = "bubble imagine " + reply
    }
    /*   for Ziggy face     only in case of speaking  */
    //if ( (say.startsWith("<span class=") != true) && reply === "") {     /*   not too clean the testing of the span text ...  */
    if (reply === "") { 
      var ziggy_face = document.createElement("span")
      ziggy_face.className = "ziggy"
      ziggy_face.innerHTML = ""
      bubble.classList.add("ziggy")
      bubble.appendChild(ziggy_face)
		}       /*   end  Ziggy face  */
    if(typeof(say)=='object'){
      var bubbleContent = document.createElement("div")
      bubbleContent.style.display = "inline-block"
      bubbleContent.className = "bubble-content"
      switch(dialogState)
      {
        case 'kpi':
            charts = create_module_data(say);
            bubbleContent.appendChild(charts);
            break;
        case 'task':
            google.charts.load('current', {'packages':['table']});
            google.charts.setOnLoadCallback(function(){
              drawTable(bubbleContent,say);
            });
            break;
        case 'cockpit':
            //charts = create_cockpit_data(say);
            charts = create_highcharts(say);
            bubbleContent.appendChild(charts);
            break;
        case 'visitor':
            charts = create_visitor_stats(say);
            bubbleContent.appendChild(charts);
            break;
        case 'qnastats':
            charts = create_qna_stats(say);
            bubbleContent.appendChild(charts);
            break;
      }
    }
    else{
      var bubbleContent = document.createElement("div")
      bubbleContent.className = "bubble-content"
      bubbleContent.innerHTML = say
    }
    bubble.appendChild(bubbleContent)
    if(category!=undefined){
      var category_text = document.createElement('p');
      category_text.classList='bubble-hidden'
      category_text.innerHTML=category;
      category_text.dataset.cate=response_count;
      bubble.appendChild(category_text);
    }
    if(dialogState=='cockpit'){
      bubbleWrap.insertBefore(bubble,bubbleTyping)
    }
    
    if((reply=='reply'&&dialogState=='Fullfilled')||dialogState=='cockpit'){
      var user_response = document.createElement('div')
      var good_answer = document.createElement('p')
      var suggest_btn = document.createElement('p')
      user_response.className = 'user-response'
      good_answer.className = 'response-btn good-btn'
      good_answer.innerHTML = '<img src="images/good-black.png" >Good Answer'
      good_answer.dataset.count = response_count
      suggest_btn.className = 'response-btn suggest-btn'
      suggest_btn.innerHTML = '<img src="images/suggest-black.png" >Support Some Suggestions'
      suggest_btn.dataset.count = response_count
      user_response.appendChild(good_answer)
      user_response.appendChild(suggest_btn)
      bubbleWrap.insertBefore(user_response,bubbleTyping)
      response_count += 1
    }
    if(dialogState!='cockpit'){
      bubbleWrap.insertBefore(bubble,bubbleTyping)
    }
    
		
    // answer picker styles
    if (reply !== "") {
      var bubbleButtons = bubbleContent.querySelectorAll(".bubble-button")

      for (var z = 0; z < bubbleButtons.length; z++) {
        ;(function(el) {
          if (!el.parentNode.parentNode.classList.contains("reply-freeform"))
            el.style.width = el.offsetWidth - sidePadding * 2 + widerBy + "px"
        })(bubbleButtons[z])
      }
      
    }
    
    // time, size & animate
    wait = animationTime * 2
    minTypingWait = animationTime * 6
    if (say.length * typeSpeed > animationTime && reply == "") {
      wait += typeSpeed * say.length
      wait < minTypingWait ? (wait = minTypingWait) : false
      setTimeout(function() {
        bubbleTyping.classList.remove("imagine")
      }, animationTime)
    }
    setTimeout(function() {
      bubbleTyping.classList.add("imagine")
    }, wait - animationTime * 2)
    bubbleQueue = setTimeout(function() {
      bubble.classList.remove("imagine")
      var bubbleWidthCalc = bubbleContent.offsetWidth + widerBy + "px"
      bubble.style.width = reply == "" ? bubbleWidthCalc : ""
      bubble.style.width = say.includes("<img src=")
        ? "50%"
        : bubble.style.width
      bubble.classList.add("say")
      posted()
      // animate scrolling
      containerHeight = container.offsetHeight
      scrollDifference = bubbleWrap.scrollHeight - bubbleWrap.scrollTop
      scrollHop = scrollDifference / 150  //change here to make the scroll slow
      var scrollBubbles = function() {
        for (var i = 1; i <= scrollDifference / scrollHop; i++) {
          ;(function() {
            setTimeout(function() {
              /*bubbleWrap.scrollHeight - bubbleWrap.scrollTop > containerHeight
                ? (bubbleWrap.scrollTop = bubbleWrap.scrollTop + scrollHop)
                : false*/
                bubbleWrap.scrollTop = bubbleWrap.scrollTop + scrollHop
            }, i * 5)
          })()
        }
      }
      setTimeout(scrollBubbles, animationTime / 2)
    }, wait + animationTime * 2)
  }
}

// below functions are specifically for WebPack-type project that work with import()

// this function automatically adds all HTML and CSS necessary for chat-bubble to function
function prepHTML(options) {
  // options
  var options = typeof options !== "undefined" ? options : {}
  var container = options.container || "chat" // id of the container HTML element
	var relative_path = options.relative_path || "./node_modules/chat-bubble/"

  // make HTML container element
  window[container] = document.createElement("div")
  window[container].setAttribute("id", container)
  document.body.appendChild(window[container])

  // style everything
  var appendCSS = function(file) {
    var link = document.createElement("link")
    link.href = file;
    link.type = "text/css"
    link.rel = "stylesheet"
    link.media = "screen,print"
    document.getElementsByTagName("head")[0].appendChild(link)
  }
	appendCSS(relative_path+ "component/styles/input.css");
	appendCSS(relative_path + "component/styles/reply.css")
	appendCSS(relative_path + "component/styles/says.css")
	appendCSS(relative_path + "component/styles/setup.css")
	appendCSS(relative_path + "component/styles/typing.css")

}

function more_click(count,question){
  $.ajax({
    url:'http://127.0.0.1:5001/v1.0/delve_more',
    data:{'limit': (more_count+1) * 20,'question':question},
    success:function(data){
      key_list = []
      sount = 1;
      for(var tmp in data){
        key_list.push(tmp)
      }
      questionsHTML = ''
      if(more_count == 0){
        start = 2;
      }
      else{
        start = more_count * 20;
      }
      console.log(data)
      console.log(key_list)
      if(key_list.length==2){
        sount = 2;
      }
      for(i=start;i<data[key_list[0]]['reply'].length;i++){
        if(key_list[i]!='score'){
          questionsHTML +=
          '<span class="bubble-button" data-reply='+reply_count+' style="animation-delay: 30ms" ' +
          'onClick="' +
          'givemeBubbles' +
          ".answer('" +
          data[key_list[0]]['reply'][i]['answer'] +
          "');this.classList.add('bubble-pick')\">" +
          data[key_list[0]]['reply'][i]['question'] +
          "</span>"
        }
      }
      if(key_list.length== (more_count+1)*20+2){
        questionsHTML += '<p class="delve_moreResult_show" data-more="'+count+'">More</p>';
      }
      $('#chat .delve_moreResult_show[data-more="'+count+'"]').parent('.bubble-content').append(questionsHTML);
      more_count +=1;
      _convo = data;
    }
  })
}


