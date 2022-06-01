#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from dtmcli import utils


def trans_call_dtm(dtm, body, operation, request_timeout):
    url = "%s/%s" % (dtm, operation)
    r = requests.post(url, json=body, timeout=request_timeout)
    utils.check_result(r)


def trans_register_branch(dtm, body, added, operation, request_timeout):
    for k, v in added.items():
        body[k] = v

    trans_call_dtm(dtm, body, operation, request_timeout)


def trans_request_branch(dtm, tb, method, body, branch_id, op, url):
    if url == "":
        return None

    query = {
        "dtm":        dtm,
        "gid":        tb.gid,
        "branch_id":  branch_id,
        "trans_type": tb.trans_type,
        "op":         op,
    }

    r = requests.request(method=method, url=url,
                         headers=tb.branch_headers, params=query, json=body)
    utils.resp_as_error_compatible(r)

    return r
