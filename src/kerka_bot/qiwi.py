from pyqiwip2p import AioQiwiP2P, QiwiP2P

from settings import QIWI_PRIV_KEY


p2p = AioQiwiP2P(auth_key=QIWI_PRIV_KEY)
p4p = QiwiP2P(auth_key=QIWI_PRIV_KEY)

async def main(num):
    new_bill = await p2p.bill(amount=num, lifetime=5)
    return (new_bill.bill_id, new_bill.pay_url)


def checking_payment(bill_id):
    return p4p.check(bill_id=bill_id).status
