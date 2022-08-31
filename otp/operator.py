from __future__ import annotations
from abc import abstractmethod,ABC




class SendSMS(ABC):

    @abstractmethod
    def sms_sender(self) -> str:
        
        pass


class SendMCI(SendSMS):

    def sms_sender(self) -> str:
        
        print("send an sms to your MCI phone number ")


class SendIrancell(SendSMS):

    def sms_sender(self) -> str:
        
        print("send an sms to your Irancell phone number ")



class FactorySMS:

    @staticmethod
    def get_sms(type):

        if type==1:
            return SendMCI()
        elif type==2:
            return SendIrancell()
