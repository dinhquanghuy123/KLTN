import hashlib
import hmac
import urllib.parse


class VNPay:

    request_data = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):

        input_data = sorted(self.request_data.items())

        query_string = urllib.parse.urlencode(input_data)

        hash_data = query_string.encode('utf-8')

        secure_hash = hmac.new(
            secret_key.encode('utf-8'),
            hash_data,
            hashlib.sha512
        ).hexdigest()

        payment_url = (
            f"{vnpay_payment_url}?"
            f"{query_string}"
            f"&vnp_SecureHashType=HmacSHA512"
            f"&vnp_SecureHash={secure_hash}"
        )

        return payment_url
