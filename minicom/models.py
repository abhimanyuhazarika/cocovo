from django.db import models

class User(models.Model):
  email = models.EmailField(max_length=254)
  name = models.TextField()
  age = models.IntegerField()
  level = models.PositiveSmallIntegerField(default=1)
  avg_time = models.IntegerField()
  correct_answers = models.PositiveSmallIntegerField(default=0)
  

  @classmethod
  def get_or_create_from_email(clazz, email, name, age):
    email = email.lower()
    try:
      return clazz.objects.get(email=email)
    except clazz.DoesNotExist:
      pass
    user = clazz(email=email,name=name,age=age,avg_time=0)
    user.save()
    return user

  @classmethod
  def get_from_email(clazz, email):
    return clazz.objects.get(email=email)

  def unread_messages(self):
    return self.message_set.filter(is_read=False, direction=Message.OUT)

  def get_last_10_messages(self):
    return self.message_set.all().order_by('-time_stamp')[:10]

  def unread_admin_messages(self):
    return self.message_set.filter(is_read=False, direction=Message.IN)

  def unread_count(self):
    return self.unread_messages().count()

  def unread_admin_count(self):
    return self.unread_admin_messages().count()

  def __unicode__(self):
    return self.email


class Message(models.Model):
  user = models.ForeignKey(User)
  message = models.TextField()
  is_read = models.BooleanField(default=False)
  time_stamp = models.DateTimeField(auto_now_add=True, db_index=True)
  direction = models.CharField(max_length=1)

  # Direction Constants
  IN = 'I'
  OUT = 'O'

  @classmethod
  def for_user_and_id(clazz, user, message_id):
    return clazz.objects.get(user=user, id=message_id)

  def mark_read(self):
    self.is_read = True
    self.save()

  def __unicode__(self):
    return "To={} Read?={} Message={}".format(self.user, self.is_read, self.message)

class Vocab(models.Model):
  word = models.TextField()
  meaning = models.TextField()
  diff_level = models.PositiveSmallIntegerField()
  is_true = models.BooleanField(default=False)


  @classmethod
  def get_vocab_from_level(clazz, level):
    return clazz.objects.filter(diff_level=level).order_by('?').first()

  @classmethod
  def get_vocab_from_vocab_id(clazz, id):
    return clazz.objects.get(id=id)


  def __unicode__(self):
    return "wodd={} meaning={} level={}".format(self.word, self.meaning, self.diff_level)


class UserVocab(models.Model):
  user = models.ForeignKey(User)
  vocab = models.ForeignKey(Vocab)
  is_correct = models.BooleanField()

  @classmethod
  def get_correct_answers_count(clazz, user_id):
    return clazz.objects.filter(user_id=user_id, is_correct=1).count()

  @classmethod
  def get_incorrect_answers_count(clazz, user_id):
    return clazz.objects.filter(user_id=user_id, is_correct=0).count()


