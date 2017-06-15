from queue import LifoQueue as Queue
from concurrent.futures import ThreadPoolExecutor as Executor
import logging
import json
import requests


class SnapService(object):
    MAX_SIZE = 0

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.queue = Queue(maxsize=SnapService.MAX_SIZE)
        self.init_workers()

    def init_workers(self):
        self.exe = Executor(max_workers=1)
        self.log.info('Init workers with work')
        self.exe.submit(self._do_work)

    def _do_work(self):
        while True:
            item = self.queue.get()
            self.log.info('Got data=%s', json.dumps(item))
            self._make_snapshot(item.get('url'))
            self.log.info('Work done.')
            self.queue.task_done()

    def _make_snapshot(self, url):
        r = requests.get(url)
        self.log.info('OUTPUT for %s=%s', url, r)
        if r.status_code == 200:
            content = r.text
            page = Page(content)
            for res in page.resources():
                if res.get('link_type') in ['link', 'script', 'css', 'style', 'img']:
                    self.log.info('resource [%s] -> %s',
                                  res['link_type'], res.get('url'))

    def add(self, request):
        self.queue.put_nowait(request)


class Page(object):

    def __init__(self, content):
        self.log = logging.getLogger(__name__)
        self.content = content
        from lxml import html
        from io import StringIO, BytesIO
        self.tree = html.parse(StringIO(content))

    def resources(self):
        links = []
        try:
            doc = self.tree.getroot()
            self.log.info(doc.iterlinks())
            for (el, attribute, link, pos) in doc.iterlinks():
                links.append(dict(element=el, link_type=el.tag, url=link))
        except Exception as e:
            print(e)
            self.log.exception(e)
        return links
