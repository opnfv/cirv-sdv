#!/usr/bin/env python

# Copyright (C) 2020 Ashwin Nayak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=abstract-method, too-many-statements

""" http server code """

import os
import json
import logging
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import tornado.concurrent
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.options
import tornado.web
import tornado.log

from cli_validation import Validate
from extrapolation import Extrapolate


class ValidateJson(RequestHandler):
    "rest api class for validation "

    def set_default_headers(self):
        """ set default headers"""
        self.set_header('Content-Type', 'application/json')

    def post(self):
        """ consume post request """
        failures = 0

        # decode the body
        data = json.loads(self.request.body.decode())

        # check for keys
        try:
            data["pdf"]
        except KeyError:
            APP_LOG.error("pdf key does not exist")
            self.write("provide pdf key\n ")
            failures += 1

        try:
            data["inst_dir"]
        except KeyError:
            APP_LOG.error("inst_dir key does not exist")
            self.write("provide inst_dir key\n")
            failures += 1

        try:
            data["inst_type"]
        except KeyError:
            APP_LOG.error("inst_type key does not exist")
            self.write("provide inst_type key\n")
            failures += 1

        try:
            data["sitename"]
        except KeyError:
            APP_LOG.error("sitename key does not exist")
            self.write("provide sitename key\n")
            failures += 1

        if failures == 0:
            pdf, inst_dir, inst_type, sitename = \
                data["pdf"], data["inst_dir"], data["inst_type"], data["sitename"]

            if inst_type not in ["airship", "tripleo"]:
                APP_LOG.error("only airship and tripleo are supported")
                self.write("only airship and tripleo are supported, for now.\n")
                failures += 1

            if failures == 0:
                result = Validate(inst_dir, inst_type, pdf, sitename).validate()
                self.write(result)


class ExtrapolateJson(RequestHandler):
    """rest api class for extrapolation"""

    def set_default_headers(self):
        """ set default header"""
        self.set_header('Content-Type', 'application/json')

    def post(self):
        """consume post request"""
        failures = 0

        data = json.loads(self.request.body.decode())

        # check for keys
        try:
            data["pdf_fn"]
        except KeyError:
            APP_LOG.error("pdf_fn key does not exist")
            self.write("provide pdf key\n ")
            failures += 1

        try:
            data["store_at"]
        except KeyError:
            APP_LOG.error("store-at key does not exist")
            self.write("provide store_at key\n ")
            failures += 1

        if failures == 0:
            pdf_fd = data["pdf_fn"]
            store_at = data["store_at"]

            # check if the paths are relative or not
            if not os.path.isabs(store_at):
                APP_LOG.critical("path provided for store_at is not an absolute path")
                self.write("provide absolute path for store_at\n ")
                failures += 1

            if failures == 0:
                try:
                    Extrapolate(pdf_fd, store_at)
                    self.write({"message": "success! New pdf file:pd_new.json"})
                except ValueError as error:
                    self.write({"message": "failure:" + str(error)})


def make_app():
    """url mapping to class """
    urls = [
        ("/validate", ValidateJson),
        ("/extrapolate", ExtrapolateJson)
    ]
    return Application(urls, debug=True)


if __name__ == '__main__':
    # app config
    APP = make_app()

    # Cli Config
    tornado.options.define("port", default=8000, help="run on the given port", type=int)
    tornado.options.parse_command_line()

    # Server Config
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(tornado.options.options.port)

    # Tornado's event loop handles it from here
    print("Starting Tornado server.....")

    # Logging
    LOG_FILE_FILENAME = "tornado.log"
    HANDLER = logging.FileHandler(LOG_FILE_FILENAME)
    APP_LOG = logging.getLogger("tornado.general")
    APP_LOG.level = logging.DEBUG
    tornado.log.enable_pretty_logging()
    APP_LOG.addHandler(HANDLER)

    # Start Loop
    tornado.ioloop.IOLoop.current().start()

    # start
    IOLoop.instance().start()
