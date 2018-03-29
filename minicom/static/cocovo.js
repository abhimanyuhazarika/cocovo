var Cocovo = {

  register: function(user_email, user_name, user_age) {
    $.post('http://localhost:8000/api/ping', {'email': user_email,'age':user_age,'name':user_name})
    .done(function(response) {
      $.each(response['unread_messages'], function(index, message) {
        //alert(message.message);
        //$("#chat_div").chatbox("option", "boxManager").addMsg("Mr. Foo", message.message);
      });
        document.getElementById("older-messages").value = response['unread_messages'].map(function(message) {return ("\n" + (message.direction+": "+message.message))});
        document.getElementById("message-id").value = response['unread_messages'].map(function(message) {return ((message.message_id))});
        //alert(document.getElementById("message-id").value);
    });
  },

//not used in cocovo
  mark_read: function(user_email, message_id) {
    $.post('http://localhost:8000/api/read', {'email': user_email, 'message_id': message_id});
  },
   
  //cocovo: used for saving user responses  
  send_admin: function(user_email, message_text, message_id) {
    $.post(
        'http://localhost:8000/api/send_admin',
        {'email': user_email, 'message_text': message_text, 'message_id':message_id}
    )
    .done(function(response) {
      $.each(response['unread_messages'], function(index, message) {
        //alert(message.message);
        //$("#chat_div").chatbox("option", "boxManager").addMsg("Mr. Foo", message.message);
       // if(message.direction=='O'){
           // Cocovo.mark_read(user_email, message.message_id);
        //}
      });
        document.getElementById("older-messages").value = response['unread_messages'].map(function(message) {return ("\n" + (message.direction+": "+message.message))});
        document.getElementById("message-id").value = response['unread_messages'].map(function(message) {return ((message.message_id))});
        //alert(document.getElementById("message-id").value);
    });
  },
  
  

};
