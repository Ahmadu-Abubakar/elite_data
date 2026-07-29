
import random

class FakeBankProvider :

    
    @staticmethod
    def create_virtual_account (user):
        account_number =  "".join (
            str(random.randint(0, 9))
            for _ in range(10)
        )

        return {
                "account_number": account_number,
                "bank_name": "Elite Bank",
                "account_name": f"EliteData - {user.username}",
                "provider_reference": f"VA-{random.randint(100000,999999)}"
            }


    @staticmethod
    def deposit_money(account_number, amount):


        return {
            "account_number": account_number,
            "amount": amount,
            "status": "SUCCESS",
            "provider_reference": f"DEP-{random.randint(100000,999999)}",
        }



