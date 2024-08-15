from enum import Enum
from abc import ABC, abstractmethod

class OPTION_TYPE(Enum):
    CALL_OPTION = "Call"
    PUT_OPTION = "Put"

class OptionPricingModel(ABC):
    " Abstract class for option pricing model "

    def calculate_option_price(self, option_type):
        " Return option price according to the specified option type "
        if option_type == OPTION_TYPE.CALL_OPTION.value:
            print("Call option price")
            return self._calculate_call_option_price()
        elif option_type == OPTION_TYPE.PUT_OPTION.value:
            return self._calculate_put_option_price()
        else:
            return -1
    
    @abstractmethod
    def _calculate_call_option_price(self):
        " Calculate call option price "
        pass

    @abstractmethod
    def _calculate_put_option_price(self):
        " Calculate put option price "
        pass