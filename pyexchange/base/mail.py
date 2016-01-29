class BaseExchangeMailService(object):

  def __init__(self, service, mail_id=None):
    self.service = service
    self.mail_id = mail_id

  def new_message(self, **properties):
    raise NotImplementedError


class BaseExchangeMailMessage(object):
  _id = None

  service = None
  mail_id = None

  recipients = []
  subject = u''
  html_body = None
  text_body = None
  attachments = None

  _track_dirty_attributes = False
  _dirty_attributes = set()  # any attributes that have changed, and we need to update in Exchange

  def __init__(self, service, id=None, mail_id=u'sentitems', **kwargs):
    self.service = service
    self._id = id
    self.mail_id = mail_id
    self._update_properties(kwargs)

  @property
  def id(self):
    return self._id

  @property
  def body(self):
    return self.html_body or self.text_body or None

  def validate(self):
    pass

  def _update_properties(self, properties):
    self._track_dirty_attributes = False
    for key in properties:
      setattr(self, key, properties[key])
    self._track_dirty_attributes = True

  def __setattr__(self, key, value):
    """ Magically track public attributes, so we can track what we need to flush to the Exchange store """
    if self._track_dirty_attributes and not key.startswith(u"_"):
      self._dirty_attributes.add(key)

    object.__setattr__(self, key, value)
