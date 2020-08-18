#!/usr/bin/env python

# Copyright (C) 2020 Ashwin Nayak <ashwinnayak111@gmail.com>

# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# pylint: disable=line-too-long, invalid-name, missing-module-docstring, broad-except

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
        except Exception:
            app_log.error("pdf key does not exist")
            self.write("provide pdf key\n ")
            failures += 1

        try:
            data["inst_dir"]
        except Exception:
            app_log.error("inst_dir key does not exist")
            self.write("provide inst_dir key\n")
            failures += 1

        try:
            data["inst_type"]
        except Exception:
            app_log.error("inst_type key does not exist")
            self.write("provide inst_type key\n")
            failures += 1
        
        try:
            data["gsw"]
        except Exception:
            app_log.error("gsw key does not exist")
            self.write("provide global_sw key\n")
            failures += 1
        
        try:
            data["tsw"]
        except Exception:
            app_log.error("tsw key does not exist")
            self.write("provide type software key\n")
            failures += 1


        if failures == 0:
            pdf, inst_dir, inst_type, gsw, tsw = data["pdf"], data["inst_dir"], data["inst_type"], data["gsw"], data["tsw"]

            # check if the paths are relative or not
            if not os.path.isabs(pdf):
                app_log.critical("path provided for pdf is not an absolute path")
                self.write("provide absolute path for pdf\n ")
                failures += 1

            if not os.path.isabs(inst_dir):
                app_log.critical("path provided for inst_dir is not an absolute path")
                self.write("provide absolute path for inst_dir\n ")
                failures += 1
            
            if not os.path.isabs(gsw):
                app_log.critical("path provided for gsw is not an absolute path")
                self.write("provide absolute path for gsw\n ")
                failures += 1
            
            if not os.path.isabs(tsw):
                app_log.critical("path provided for tsw is not an absolute path")
                self.write("provide absolute path for tsw\n ")
                failures += 1

            if inst_type not in ["airship", "tripleo"]:
                app_log.error("only airship and tripleo are supported")
                self.write("only airship and tripleo are supported, for now.\n")
                failures += 1

            if failures == 0:
                result = Validate(inst_dir, inst_type, pdf, gsw, tsw).validate()
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
        except Exception:
            app_log.error("pdf_fn key does not exist")
            self.write("provide pdf key\n ")
            failures += 1

        try:
            data["store_at"]
        except Exception:
            app_log.error("store-at key does not exist")
            self.write("provide store_at key\n ")
            failures += 1

        if failures == 0:
            pdf_fd = data["pdf_fn"]
            store_at = data["store_at"]

            # check if the paths are relative or not
            if not os.path.isabs(pdf_fd):
                app_log.critical("path provided for pdf is not an absolute path")
                self.write("provide absolute path for pdf\n ")
                failures += 1

            if not os.path.isabs(store_at):
                app_log.critical("path provided for store_at is not an absolute path")
                self.write("provide absolute path for store_at\n ")
                failures += 1

            if failures == 0:
                try:
                    Extrapolate(pdf_fd, store_at)
                    self.write({"message": "success! New pdf file:pd_new.json"})
                except Exception as e:
                    self.write({"message": "failure:"+str(e)})

def make_app():
    """url mapping to class """
    urls = [
        ("/validate", ValidateJson),
        ("/extrapolate", ExtrapolateJson)
    ]
    return Application(urls, debug=True)

if __name__ == '__main__':
    # app config
    app = make_app()

    # Cli Config
    tornado.options.define("port", default=8000, help="run on the given port", type=int)
    tornado.options.parse_command_line()

    # Server Config
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)

    # Tornado's event loop handles it from here
    print("Starting Tornado server.....")

    # Logging
    log_file_filename = "tornado.log"
    handler = logging.FileHandler(log_file_filename)
    app_log = logging.getLogger("tornado.general")
    app_log.level = logging.DEBUG
    tornado.log.enable_pretty_logging()
    app_log.addHandler(handler)

    # Start Loop
    tornado.ioloop.IOLoop.current().start()

    # start
    IOLoop.instance().start()
