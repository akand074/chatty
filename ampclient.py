from twisted.internet import reactor, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp
from ampserver import Sum, Divide


def doMath():
    creator = ClientCreator(reactor, amp.AMP)

    cmdDeferred = creator.connectTCP('127.0.0.1', 1234)

    def connected(ampProto):
        oper = raw_input("Please enter the type of operation (sum or divide): ")
        if oper.lower() == "sum":
            vals = raw_input("Please enter two integers separated by a space: ")
            x,y = [int(i) for i in vals.split(' ')]
            cmdDeferred.addCallback(summed)
            return ampProto.callRemote(Sum, a=x, b=y)
        elif oper.lower() == "divide":
            vals = raw_input("Please enter the numerator then the denominator as integers separated by a space: ")
            x,y = [int(i) for i in vals.split(' ')]
            cmdDeferred.addCallback(divided)
            cmdDeferred.addErrback(trapZero)
            return ampProto.callRemote(Divide, n=x, d=y)
        else:
            print "Invalid command."
            return False
    cmdDeferred.addCallback(connected)

    def summed(result):
        return result['total']

    def divided(result):
        return result['quotient']
    
    def trapZero(result):
        result.trap(ZeroDivisionError)
        print "Divided by zero: returning INF"
        return 1e1000

    def done(result):
        if result == True:
            print 'Done with math:', result
        reactor.stop()
    defer.DeferredList([cmdDeferred]).addCallback(done)

if __name__ == '__main__':
    doMath()
    reactor.run()