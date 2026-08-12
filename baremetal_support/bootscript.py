# Copyright (C) 2019-2021 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

import socket

from bottle import request, response


class BootscriptNotFound(Exception):
    """Raised when the address is invalid"""


class Bootscript:
    def __init__(self, app, logger):
        self.bootscript = {}
        self._app = app
        self.log = logger
        self._app.route(
            "/v1/bootscript/script.ipxe",
            method="GET",
            callback=self.http_get_bootscript_for_peer,
        )
        self._app.route(
            "/v1/bootscript/script.ipxe/<addr>",
            method="POST",
            callback=self.http_set_bootscript,
        )
        self._app.route(
            "/v1/bootscript/script.ipxe/<addr>",
            method="GET",
            callback=self.http_get_bootscript,
        )

    def set(self, ip, script):
        """set the bootscript in the dict"""
        self.log.info("setting bootscript for " + ip)
        self.log.debug(script)
        self.bootscript[ip] = script

    def get(self, ip):
        """return specific bootscript"""
        try:
            self.log.info("retrieving bootscript for " + ip)
            return self.bootscript[ip]
        except KeyError:
            self.log.error("no script found for " + ip)
            raise BootscriptNotFound("no script found for requested ip")

    def _is_ip(self, addr):
        try:
            socket.inet_aton(addr)
            return True
        except OSError:
            return False

    def http_get_bootscript_for_peer(self):
        addr = request.environ.get("REMOTE_ADDR")
        self.log.debug("http request: get bootscript for peer (" + addr + ")")
        return self.http_get_bootscript(addr)

    def http_get_bootscript(self, addr):
        try:
            if self._is_ip(addr):
                response.content_type = "text/text; charset=utf-8"
                self.log.debug("http request: get bootscript for " + addr)
                return self.get(addr)
            else:
                # invalid address specified
                response.status = 400
        except BootscriptNotFound:
            # no script found for this IP
            self.log.debug("http request: no bootscript found for " + addr)
            response.body = "not found"
            response.status = "404 Not Found"
            return response

    def http_set_bootscript(self, addr):
        if self._is_ip(addr):
            postdata = request.body.read()
            script = postdata.decode("utf-8")
            self.log.info("http request: set bootscript for " + addr)
            self.log.debug(script)
            self.set(addr, script)
            response.status = 200
        else:
            self.log.debug("http request: not setting bootscript, invalid address given: " + addr)
            response.status = 400
