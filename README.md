# Trend-Tides
tracks financial markets tickers and sends alerts of trend changes.

### Config
This app/script needs access to smtp email account to send the email message out to the appropriate email to sms email address the user needs to use.
.env variables that will need to be set are the email address and password you are using to send the outbound email, the smtp sever address and port, and the email address that your cell carrier uses to
convert an email into a text message. 

### Useage
The script is designed to run in an always on environment. Once running, it will check what time it is and between 12-13 UTC it will access the Yahoo finance data of the selected tickers, 
USDX (U.S. Dollar Index), S&P 500, Bitcoin, and Ethereum. It is a long term looking monitoring device. It looks at longer term market trends over a period of a few months 
using what amounts to a linear regression trend slope and if the trend goes from positive to negative or negative to positive it will issue an alert
that the trend has changed. If no trend change was detected, it will still send an update alert once a week on Wednesday.

