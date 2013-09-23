var chat_room_id = undefined;
var last_received = 0;

/**
 * Initialize chat:
 * - Set the room id
 * - Generate the html elements (chat box, forms & inputs, etc)
 * - Sync with server
 * @param chat_room_id the id of the chatroom
 * @param html_el_id the id of the html element where the chat html should be placed
 * @return
 */

var timer;

Date.prototype.setISO8601 = function (string) {
    var regexp = "([0-9]{4})(-([0-9]{2})(-([0-9]{2})" +
        "(T([0-9]{2}):([0-9]{2})(:([0-9]{2})(\.([0-9]+))?)?"+
        "(Z|(([-+])([0-9]{2}):([0-9]{2})))?)?)?)?";
    var d = string.match(new RegExp(regexp));

    var offset = 0;
    var date = new Date(d[1], 0, 1);

    if (d[3]) { date.setMonth(d[3] - 1); }
    if (d[5]) { date.setDate(d[5]); }
    if (d[7]) { date.setHours(d[7]); }
    if (d[8]) { date.setMinutes(d[8]); }
    if (d[10]) { date.setSeconds(d[10]); }
    if (d[12]) { date.setMilliseconds(Number("0." + d[12]) * 1000); }
    if (d[14]) {
        offset = (Number(d[16]) * 60) + Number(d[17]);
        offset *= ((d[15] == '-') ? 1 : -1);
    }

    offset -= date.getTimezoneOffset();
    time = (Number(date) + (offset * 60 * 1000));
    this.setTime(Number(time));
}
function init_chat(chat_id, html_el_id) {
	chat_room_id = chat_id;
	layout_and_bind(html_el_id);
	sync_messages();
	chat_join();
}
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
	});
	
var img_dir = "/static/img/";

/**
 * Asks the server which was the last message sent to the room, and stores it's id.
 * This is used so that when joining the user does not request the full list of
 * messages, just the ones sent after he logged in. 
 * @return
 */
function sync_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id},
        url:'/chat/sync/',
		dataType: 'json',
		csrfmiddlewaretoken: '{{ csrf_token }}',  
		success: function (json) {
        	last_received = json.last_message_id;
		}        
    });
	
	setTimeout("get_messages()", 2000);
}

/**
 * Generate the Chat box's HTML and bind the ajax events
 * @param target_div_id the id of the html element where the chat will be placed 
 */
function layout_and_bind(html_el_id) {
		// layout stuff
		var html = '<div id="chat-messages-container">'+
		'<div id="chat-messages"> <a href="#" id="load_chat_history">Load history</a> </div>'+
		'<div id="chat-last"></div>'+
		'</div>'+
		'<form id="chat-form">'+
		'<input name="message" type="text" class="message" />'+
		'<input type="submit" value="Say!!!" class="button orange" />'+
		'<input id="chat_logout" type="button" value="Logout" class="button orange" />'+
		'</form>';
		
		$("#"+html_el_id).append(html);
		$('#chat_logout').click(function(event){
			event.preventDefault();
			chat_leave();
			$.cookie('dchat_name',null);
			clearTimeout(timer);
			$('#chat').fadeOut(300, function(){ $('#chat').empty();$('#fchat').fadeIn(300,function(){
				var ch = $('#chat_container').height()+20;
			var ih = $('#info_container').height()+20;
			var fh = $('#filetree_container').height()+20;
    		var oh = $('.equal_height').height();
   			var max = Math.max(ch,ih,fh);
   			if(max != oh){
   				$('.equal_height').animate({height:max}); 
   			}});});
			
		});
		// event stuff
    	$("#chat-form").submit( function () {
            var $inputs = $(this).children('input');
            var values = {};
            
            $inputs.each(function(i,el) { 
            	values[el.name] = $(el).val();
            });
			values['chat_room_id'] = window.chat_room_id;
        	$.ajax({
                data: values,
                dataType: 'json',
                csrfmiddlewaretoken: '{{ csrf_token }}',  
                type: 'post',
                url: '/chat/send/'
            });
            $('#chat-form .message').val('');
            return false;
	});
	$('a#load_chat_history').click(function(e){
		e.preventDefault();
		get_messages(true);
	});
};

/**
 * Gets the list of messages from the server and appends the messages to the chatbox
 */

function get_messages(all_messages) {
	all_messages = typeof all_messages !== 'undefined' ? all_messages : false;
	if (all_messages){
		$('#chat-messages').empty();
		data = {id:window.chat_room_id, offset: 0}
	}else{
	data = {id:window.chat_room_id, offset: window.last_received}
	}
    $.ajax({
        type: 'POST',
        data: data,
        url:'/chat/receive/',
		dataType: 'json',
		csrfmiddlewaretoken: '{{ csrf_token }}',  
		success: function (json) {
			var scroll = false;
		
			// first check if we are at the bottom of the div, if we are, we shall scroll once the content is added
			var $containter = $("#chat-messages-container");
			//console.log($containter[0].scrollHeight+'=='+$containter.scrollTop()+' + '+$containter.innerHeight());
			if ($containter[0].scrollHeight == $containter.scrollTop()+$containter.innerHeight())
				scroll = true;	

			// add messages
			$.each(json, function(i,m){
				var time = new Date();
				time.setISO8601(m.timestamp);
				console.log(time);
				var timestr = ("0" + time.getUTCHours()).slice(-2)+':'+("0" + time.getUTCMinutes()).slice(-2)+' ';
				if (m.type == 's')
					$('#chat-messages').append('<div class="system">' + timestr+ replace_emoticons(m.message) + '</div>');
				else if (m.type == 'm') 	
					$('#chat-messages').append('<div class="message">'+timestr +'<div class="author">'+m.author+'</div>'+replace_emoticons(m.message) + '</div>');
				else if (m.type == 'j') 	
					$('#chat-messages').append('<div class="join">'+timestr+' '+m.author+' has joined</div>');
				else if (m.type == 'l') 	
					$('#chat-messages').append('<div class="leave">'+timestr+' '+m.author+' has left</div>');
				else if (m.type == 'c') 	
					$('#chat-messages').append('<div class="command">'+timestr+'<div class="author">'+m.author+'</div>'+ m.message +'</div>');	
				last_received = m.id;
			})
			
			// scroll to bottom
			if (scroll)
				$("#chat-messages-container").animate({ scrollTop: $("#chat-messages-container").prop("scrollHeight") }, 500);
		}        
    });
    
    // wait for next
    timer = setTimeout("get_messages()", 2000);
}


/**
 * Tells the chat app that we are joining
 */
function chat_join() {
	$.ajax({
		async: false,
        type: 'POST',
        csrfmiddlewaretoken: '{{ csrf_token }}',  
        data: {chat_room_id:window.chat_room_id},
        url:'/chat/join/',
    });
}

/**
 * Tells the chat app that we are leaving
 */
function chat_leave() {
	$.ajax({
		async: false,
        type: 'POST',
        csrfmiddlewaretoken: '{{ csrf_token }}',  
        data: {chat_room_id:window.chat_room_id},
        url:'/chat/leave/',
    });
}

// attach join and leave events
//$(window).load(function(){chat_join()});
$(window).unload(function(){chat_leave()});

// emoticons
var emoticons = {                 
	'>:D' : 'emoticon_evilgrin.png',
	':D' : 'emoticon_grin.png',
	'=D' : 'emoticon_happy.png',
	':\\)' : 'emoticon_smile.png',
	':O' : 'emoticon_surprised.png',
	':P' : 'emoticon_tongue.png',
	':\\(' : 'emoticon_unhappy.png',
	':3' : 'emoticon_waii.png',
	';\\)' : 'emoticon_wink.png',
	'\\(ball\\)' : 'sport_soccer.png'
}

/**
 * Regular expression maddness!!!
 * Replace the above strings for their img counterpart
 */
function replace_emoticons(text) {
	$.each(emoticons, function(char, img) {
		re = new RegExp(char,'g');
		// replace the following at will
		text = text.replace(re, '<img src="'+img_dir+img+'" />');
	});
	text = text.replace(/#\w*/g,'<span class="tag">$&</span>');
	return text;
}