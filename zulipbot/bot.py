import zulip

from zulipbot.commands import *
from zulipbot.msg import *


class ZulipBot(object):
    """get messages, process, reply"""

    def __init__(self, client: zulip.Client, msg_filter: dict):
        self.client = client
        self.msg_filter = msg_filter
        self.cmds: list[ZulipBotCmdBase] = []
        self.add_cmd(ZulipBotCmdHelp(self.cmds))

    def add_cmd(self, cmd: ZulipBotCmdBase):
        self.cmds.append(cmd)

    def run_callback(self, m):
        msg = ZulipMsg(self.client, self.msg_filter, m)
        for cmd in self.cmds:
            if cmd.is_to_be_processed(msg):
                cmd.process(msg)

    def run(self):
        self.client.call_on_each_message(self.run_callback)
