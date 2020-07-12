from message import *

class MessageEncoder():
    def _encode_message(self, payload, suffix=b'\xff\xff'):
        message = b'\x0f'

        message += (len(payload)+1).to_bytes(1, 'big')
        message += payload

        message += ((1+sum(payload)) & 0xff).to_bytes(1, 'big')
        message += suffix

        return message

    def _encode_pin(self, pin):
            pin_bytes = b''
            for i in pin:
                pin_bytes += int(i).to_bytes(1, 'big')
            
            return pin_bytes

    def encode(self, message):
        if isinstance(message, AuthorizeCommand):
            pin = self._encode_pin(message.pin)
            return self._encode_message(b'\x17\x00\x00' + pin + b'\x00\x00\x00\x00')

        if isinstance(message, ChangePinCommand):
            pin = self._encode_pin(message.pin)
            new_pin = self._encode_pin(message.new_pin)
            return self._encode_message(b'\x17\x00\x01' + new_pin + pin)

        if isinstance(message, ResetPinCommand):
            return self._encode_message(b'\x17\x00\x02' + b'\x00\x00\x00\x00\x00\x00\x00\x00')

        if isinstance(message, PowerSwitchCommand):
            if message.on:
                return self._encode_message(b'\x03\x00\x01' + b'\x00\x00')
            else:
                return self._encode_message(b'\x03\x00\x00' + b'\x00\x00')

        if isinstance(message, LEDSwitchCommand):
            if message.on:
                return self._encode_message(b'\x0f\x00\x05\x01' + b'\x00\x00\x00\x00')
            else:
                return self._encode_message(b'\x0f\x00\x05\x00' + b'\x00\x00\x00\x00')

        if isinstance(message, SynchronizeDateAndTimeCommand):
            year = message.year.to_bytes(2, 'big')
            month = message.month.to_bytes(1, 'big')
            day = message.day.to_bytes(1, 'big')

            hour = message.hour.to_bytes(1, 'big')
            minute = message.minute.to_bytes(1, 'big')
            second = message.second.to_bytes(1, 'big')

            return self._encode_message(b'\x01\x00' + second + minute + hour + day + month + year + b'\x00\x00')

        if isinstance(message, AuthorizationNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x00\x00')

        if isinstance(message, ChangePinNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x01\x00')

        if isinstance(message, ResetPinNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x02\x00')

        if isinstance(message, PowerSwitchNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x03\x00' + was_successful)

        if isinstance(message, LEDSwitchNotification):
            return self._encode_message(b'\x0f\x00' + b'\x05\x00')

        if isinstance(message, SynchronizeDateAndTimeNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x01\x00' + was_successful)


        raise Exception('Unsupported message ' + str(message))

