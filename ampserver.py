from twisted.protocols import amp

class Sum(amp.Command):
    arguments = [('a', amp.Integer()),
                 ('b', amp.Integer())]
    response = [('total', amp.Integer())]


class Divide(amp.Command):
    arguments = [('n', amp.Integer()),
                 ('d', amp.Integer())]
    response = [('quotient', amp.Float())]
    errors = {ZeroDivisionError: 'ZERO_DIVISION'}


class Math(amp.AMP):
    def sum(self, a, b):
        total = a + b
        print 'Did a sum: %d + %d = %d' % (a, b, total)
        return {'total': total}
    Sum.responder(sum)

    def divide(self, n, d):
        quotient = float(n) / d
        print 'Divided: %d / %d = %f' % (n, d, quotient)
        return {'quotient': quotient}
    Divide.responder(divide)


def main():
    from twisted.internet import reactor
    from twisted.internet.protocol import Factory
    pf = Factory()
    pf.protocol = Math
    reactor.listenTCP(1234, pf)
    print 'started'
    reactor.run()

if __name__ == '__main__':
    main()