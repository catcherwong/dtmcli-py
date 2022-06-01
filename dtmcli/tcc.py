#!/usr/bin/python
# -*- coding: UTF-8 -*-

import traceback
import sys
import json
from dtmcli import dtmimp, transbase, utils


class Tcc(object):
    def __init__(self, dtmUrl, gid):
        self.dtm = dtmUrl
        self.trans_base = transbase.TransBase(gid, "tcc")
        self.id_generator = utils.IdGenerator()

    def call_branch(self, body, tryUrl, confirmUrl, cancalUrl):
        branch_id = self.id_generator.new_branch_id()

        tb = {
            "gid": self.trans_base.gid,
            "trans_type": self.trans_base.trans_type,
            "custom_data": self.trans_base.custom_data,
        }

        added = {
            "data":          json.dumps(body),
            "branch_id":      branch_id,
            "confirm": confirmUrl,
            "cancel": cancalUrl,
        }

        dtmimp.trans_register_branch(
            self.dtm, body=tb, added=added, operation="registerBranch", request_timeout=8)

        r = dtmimp.trans_request_branch(
            self.dtm, self.trans_base, "POST", body, branch_id, "try", tryUrl)

        return r


def tcc_global_transaction(dtmUrl, gid, tcc_cb):
    return tcc_global_transaction2(dtmUrl, gid, lambda t: None, tcc_cb)


def tcc_global_transaction2(dtmUrl, gid, custom, tcc_cb):
    tcc = Tcc(dtmUrl, gid)
    custom(tcc)

    try:
        dtmimp.trans_call_dtm(tcc.dtm, tcc.trans_base.__dict__,
                              "prepare", tcc.trans_base.request_timeout)
        tcc_cb(tcc)
        dtmimp.trans_call_dtm(tcc.dtm, tcc.trans_base.__dict__,
                              "submit", tcc.trans_base.request_timeout)
    except:
        traceback.print_exception(*sys.exc_info())
        dtmimp.trans_call_dtm(tcc.dtm, tcc.trans_base.__dict__,
                              "abort", tcc.trans_base.request_timeout)
        return ""
    return gid


def tcc_from_req(dtmUrl, gid, branch_id):
    if dtmUrl == "" or gid == "" or branch_id == "":
        raise Exception("bad tcc req info: dtm %s gid %s branch_id %s" % (
            dtmUrl, gid, branch_id))
    tcc = Tcc(dtmUrl, gid)
    tcc.id_generator = utils.IdGenerator(branch_id)
    return tcc
