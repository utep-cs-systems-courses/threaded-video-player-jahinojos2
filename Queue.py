#!/usr/bin/env python3

import threading


class Queue():
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.full =  threading.Semaphore(0)
        self.empty =  threading.Semaphore(24)

    def put(self, item):
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.full.release()

    def get(self):
        self.full.acquire()
        self.lock.acquire()
        item = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return item

