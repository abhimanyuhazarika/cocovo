import json

from django.http import HttpResponse

from models import User, Message,Vocab,UserVocab

def render_to_json(content, **kwargs):
  return HttpResponse(json.dumps(content), content_type='application/json', **kwargs)


def ping(request):
  email = request.POST.get('email', None)
  age = request.POST.get('age', None)
  name = request.POST.get('name', None)
  
  if not email:
    return render_to_json({'error': 'Missing required parameter: email.'}, status=400)
  user = User.get_or_create_from_email(email,name,age)
  level = user.level
 
  unread_messages = []
  question = Vocab.get_vocab_from_level(level=level)
  unread_messages.append({
      'message_id': question.id,
      'message': question.word+' \n:'+question.meaning,
      'direction': 'Level-'+str(level)+' \n:'})

  return render_to_json({
    'email': user.email,
    'unread_messages': unread_messages,})


def mark_as_read(request):
  message_id = request.POST.get('message_id', None)
  email = request.POST.get('email', None)
  if not (email and message_id):
    return render_to_json({'error': 'Missing required parameters: email, message_id.'}, status=400)

  try:
    message = Message.for_user_and_id(User.get_from_email(email), message_id)
  except User.DoesNotExist:
    return render_to_json({'error': 'No user found with that address.'}, status=404)
  except Message.DoesNotExist:
    return render_to_json({'error': 'No message found with that id.'}, status=404)

  message.mark_read()
  return render_to_json({'success': 'Marked as read.'})


def send_message(request):
  to_user = request.POST.get('to_user', None)
  message_text = request.POST.get('message', None)
  direction = Message.OUT
  if not (to_user and message_text):
    return render_to_json({'error': 'Missing required parameters: to_user, message.'}, status=400)

  user = User.get_or_create_from_email(to_user)
  message = Message(user=user, message=message_text, direction=direction)
  message.save()

  return render_to_json({'success': 'Your message was sent.'})


def send_message_to_admin(request):
  email = request.POST.get('email', None)
  message_text = request.POST.get('message_text', None)
  vocab_id = request.POST.get('message_id', None)
  if not email:
    return render_to_json({'error': 'Missing required parameter: email.'}, status=400)
  if not message_text:
    return render_to_json({'error': 'Missing required parameter: message.'}, status=400)
  #user = User.get_or_create_from_email(email)
  vocab = Vocab.get_vocab_from_vocab_id(id=vocab_id)
  vocab_is_true = vocab.is_true
  user = User.get_or_create_from_email(email,'null','null')
  #user_level = user.level
  if vocab_is_true and message_text=='1':
    user_vocab = UserVocab(user=user, vocab=vocab, is_correct=1)
    user_vocab.save()
    user = User.get_or_create_from_email(email,'null','null')
    user_level = user.level
    unread_messages = []
    question = Vocab.get_vocab_from_level(level=user_level)
    unread_messages.append({
      'message_id': question.id,
      'message': question.word+' \n:'+question.meaning,
      'direction': 'Level-'+str(user_level)+' \n:'})

    return render_to_json({
      'email': user.email,
      'unread_messages': unread_messages,})    
    #return render_to_json({'success': message_text })
  else:
    user_vocab = UserVocab(user=user, vocab=vocab, is_correct=0)
    user_vocab.save()
    return render_to_json({'failed': message_text })

  unread_messages = []
  question = Vocab.get_vocab_from_level(level=level)
  unread_messages.append({
      'message_id': question.id,
      'message': question.word+' \n:'+question.meaning,
      'direction': 'I'})

  return render_to_json({
    'email': user.email,
    'unread_messages': unread_messages,})


def n_last_messages(request):
  email = request.POST.get('email', None)
  if not email:
    return render_to_json({'error': 'Missing required parameter: email.'}, status=400)
  user = User.get_or_create_from_email(email)
  messages = user.get_last_10_messages()
  return render_to_json({'messages': "\n".join([(message.direction+": "+ message.message) for message in messages])})