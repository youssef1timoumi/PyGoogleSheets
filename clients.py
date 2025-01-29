class Client:
    def __init__(self, id, full_name, service, payment, paid, code=None, solde=0):
        self.id = id
        self.full_name = full_name
        self.service = service
        self.payment = float(payment)
        self.paid = paid
        self.code = code if code else ""  # Default empty string if no code provided
        self.solde = float(solde)  # Default is 0 if not provided

    def marketing_revenue(self):
        if self.code:  # Calculate revenue only if the client has a referral code
            print("Client found!:", self.full_name)
            return self.payment * 0.2  # 20% of payment
        else:
            return 0  # No revenue if no referral code

    def calculate_payment(self):
        if self.solde != 0:
            return self.payment-self.solde  # 10% of solde
        else:
            return self.payment

    def calculate_revenue(self):
        tmp = float(self.calculate_payment() + self.marketing_revenue())
        return tmp
    