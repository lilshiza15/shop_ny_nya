import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AeBqsigEh7q6J4kA4-_ZchW31IIySKieN0iQR9ThqcEderDZUY-4WAn9KAkXoq0CDlVCbvtmaYO3oC6Y"
        self.client_secret = "EJWZ0_VCMwYGW99v7UyiiCL0zDQT0ookyLcyd55gJcXMtUU0RtXiN9qhRkUdOKtTRO2KJAbG0bZegCYx"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)