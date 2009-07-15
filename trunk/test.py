#!/usr/bin/python

from pymine.core.mine import Mine

if __name__ == '__main__':

    user = "alecm"

    m = Mine(user)

    t = m.items.Open(30)
    print t.Describe('itemName')

    v = t.Get('itemName')
    print v

    m2 = Mine("adriana")

    t2 = m2.items.Open(30)
    print t2.Describe('itemName')

    v2 = t2.Get('itemName')
    print v2

