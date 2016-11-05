This package leverages Zappa - Serverless Python Web Services
@see https://www.zappa.io/
@see https://github.com/Miserlou/Zappa

Zappa makes it super easy to deploy all Python WSGI applications on AWS Lambda + API Gateway.
Think of it as "serverless" web hosting for your Python web apps. That means infinite scaling,
zero downtime, zero maintenance - and at a fraction of the cost of your current deployments!

Before using the Zappa tool, you will need to setup an AWS account on your system. Once
setup, issue the 'zappa deploy dev' instruction from the command line to initially upload
this Python Flask module.  Updates can later issue the 'zappa update dev' instruction from
the command line.

Note:  Zappa commands should be issued while the Python virtualenv is activated in the
command prompt