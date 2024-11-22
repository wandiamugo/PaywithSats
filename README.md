#Features

##User Onboarding

- Create New Wallet: Users can create a new wallet and receive a recovery phrase for secure access.
- Recover Wallet: Recover an existing wallet using a recovery phrase.
  
##Wallet Dashboard

- Displays Bitcoin and Lightning balances.
- Send and receive payments for Bitcoin and Lightning.
- Backup functionality to securely store recovery phrases.
- Receive Payments

- Send Bitcoin to any address using sendtoaddress.
- Send Lightning payments using lncli sendpayment.
- Transaction Status and Confirmation

##API Endpoints

#Wallet Management

 `POST /create-wallet: Create a new wallet and return recovery information.`

`POST /recover-wallet: Recover an existing wallet using a recovery phrase.`

`POST /backup-wallet: Retrieve wallet recovery information.
Transaction Handling`

`POST /send-payment: Send Bitcoin to a recipient.`

`POST /send-lightning-payment: Process Lightning payments.`

`GET /generate-address: Generate a new Bitcoin address.`

`GET /generate-lightning-invoice: Generate a Lightning invoice.`

`GET /check-transaction-status/:txid: Check Bitcoin transaction status.`

`GET /check-lightning-payment-status/:invoiceId: Check Lightning 
transaction status.Wallet Balance`

`GET /get-balance: Fetch Bitcoin and Lightning wallet balances.`


##Setup Steps

- git clone https://github.com/yourusername/coder-girlies-payment-system.git
- cd coder-girlies-payment-system
  
#Install dependencies:

pip install -r requirements.txt

CONTRIBUTORS 

[@sawe-daisy](https://github.com/sawe-daisy)

[@grace-mugoiri](https://github.com/grace-mugoiri)

[@wandiamugo](https://github.com/wandiamugo)

[@brendaoduor](https://github.com/brendaoduor)

[@victoriandicu](https://github.com/victoriandicu)

[@salhabenazir](https://github.com/salhabenazir)

[@vera_wuor](https://github.com/vera_wuor)


