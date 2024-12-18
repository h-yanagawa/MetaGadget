from switchbot_client.case_insensitive_invoke_mixin import CaseInsensitiveInvokeMixin
from switchbot_client.switchbot_base_client import SwitchBotBaseClient
from switchbot_client.switchbot_mixin import SwitchBotDeviceOpsMixin


class SwitchBotClient(SwitchBotBaseClient, SwitchBotDeviceOpsMixin, CaseInsensitiveInvokeMixin):
    def __init__(self, token: str, secret: str):
        # 多重継承した場合、super()は最初に指定したクラスのメソッドを呼び出すのでsuperで1個ずらしで呼び出すと、
        # SwitchBotBaseClient -> SwitchBotClientMixin -> CaseInsensitiveInvokeMixin の順に__init__()が呼び出される
        # When multiple inheritance, super() calls the method of the first specified class, so if you call it with a shift of one with super(),
        # __init__() is called in the order of SwitchBotBaseClient -> SwitchBotClientMixin -> CaseInsensitiveInvokeMixin
        super(SwitchBotClient, self).__init__(token, secret) # SwitchBotBaseClient.__init__(self, token, secret)
        super(SwitchBotBaseClient, self).__init__() # SwitchBotClientMixin.__init__(self)
        super(SwitchBotDeviceOpsMixin, self).__init__() # CaseInsensitiveInvokeMixin.__init__(self)

