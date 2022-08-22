from abc import ABC
from abc import abstractmethod




class SendSMS(ABC):

    @abstractmethod
    def sms_sender(self) -> str:
        
        pass


class SendMCI(SendSMS):

    def sms_sender(self) -> str:
        
        return "send an sms to your MCI phone number "


class SendIrancell(SendSMS):

    def sms_sender(self) -> str:
        
        return "send an sms to your Irancell phone number "


