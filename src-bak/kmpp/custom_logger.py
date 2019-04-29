# source ; https://gist.github.com/NelsonMinar/74d94f8bcb78fae150e3

import logging, os

logger = logging.getLogger("kmpp")

class MultiHandler(logging.Handler):
  def __init__(self, dirname):
    super(MultiHandler, self).__init__()
    self.files = {}
    self.dirname = dirname
    if not os.access(dirname, os.W_OK):
      raise Exception("Directory %s not writeable" % dirname)

  def flush(self):
    self.acquire()
    try:
      for fp in self.files.values():
        fp.flush()
    finally:
      self.release()

  def _get_or_open(self, key):
    "Get the file pointer for the given key, or else open the file"
    self.acquire()
    try:
      if key in self.files:
        return self.files[key]
      else:
        fp = open(os.path.join(self.dirname, "%s.log" % key), "w")
        self.files[key] = fp
        return fp
    finally:
      self.release()

  def emit(self, record):
    try:
      fp = self._get_or_open(record.threadName)
      msg = self.format(record)
      fp.write('%s\n' % msg.encode("utf-8"))
    except (KeyboardInterrupt, SystemExit):
      raise
    except:
      self.handleError(record)

log_format = '[%(levelname).1s] %(threadName)12s: %(message)s'
stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(stderr_handler)

multi_handler = MultiHandler("../log")
multi_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(multi_handler)

logger.setLevel(logging.DEBUG)