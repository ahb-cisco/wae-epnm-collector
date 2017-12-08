import com.cisco.wae.design
from com.cisco.wae.design.model.net import HopType
# keys
from com.cisco.wae.design.model.net import NodeKey
from com.cisco.wae.design.model.net import InterfaceKey
from com.cisco.wae.design.model.net.layer1 import L1NodeKey
from com.cisco.wae.design.model.net.layer1 import L1PortKey
from com.cisco.wae.design.model.net.layer1 import L1CircuitKey
from com.cisco.wae.design.model.net.layer1 import L1CircuitPathKey
# records
from com.cisco.wae.design.model.net import NodeRecord
from com.cisco.wae.design.model.net.layer1 import L1NodeRecord
from com.cisco.wae.design.model.net.layer1 import L1LinkRecord
from com.cisco.wae.design.model.net.layer1 import L1PortRecord
from com.cisco.wae.design.model.net.layer1 import L1CircuitRecord
from com.cisco.wae.design.model.net.layer1 import L1CircuitPathRecord
from com.cisco.wae.design.model.net.layer1 import L1CircuitPathHopRecord
from com.cisco.wae.design.model.net import InterfaceRecord
from com.cisco.wae.design.model.net import CircuitRecord


def generateL1nodes(plan, l1nodelist):
    l1NodeManager = plan.getNetwork().getL1Network().getL1NodeManager()
    for l1node in l1nodelist:
        l1nodeRec = L1NodeRecord(name=l1node)
        l1NodeManager.newL1Node(l1nodeRec)


def generateL1links(plan, l1linklist):
    l1LinkManager = plan.getNetwork().getL1Network().getL1LinkManager()
    for l1link in l1linklist:
        l1nodeAKey = L1NodeKey(l1link[0])
        l1nodeBKey = L1NodeKey(l1link[1])
        l1linkname = l1link[0] + "_" + l1link[1]
        l1linkRec = L1LinkRecord(name=l1linkname, l1NodeAKey=l1nodeAKey, l1NodeBKey=l1nodeBKey)
        l1LinkManager.newL1Link(l1linkRec)


def generateL1circuit(plan, name, l1nodeA, l1nodeB, l1hops, bw):
    l1portManager = plan.getNetwork().getL1Network().getL1PortManager()
    # l1portrecs = l1portManager.getAllL1PortRecords()
    l1nodeAKey = L1NodeKey(l1nodeA)
    l1nodeBKey = L1NodeKey(l1nodeB)
    l1portAname = name + '_port_to_' + l1nodeB
    l1portBname = name + '_port_to_' + l1nodeA
    l1portRecA = L1PortRecord(name=l1portAname, l1Node=l1nodeAKey)
    l1portRecB = L1PortRecord(name=l1portBname, l1Node=l1nodeBKey)

    l1portManager.newL1Port(l1portRecA)
    l1portManager.newL1Port(l1portRecB)

    l1portAkey = L1PortKey(name=l1portAname, l1Node=l1nodeAKey)
    l1portBkey = L1PortKey(name=l1portBname, l1Node=l1nodeBKey)

    l1circuitrec = L1CircuitRecord(name=name, l1PortAKey=l1portAkey, l1PortBKey=l1portBkey,bandwidth=bw)

    l1circuitManager = plan.getNetwork().getL1Network().getL1CircuitManager()
    l1circuit = l1circuitManager.newL1Circuit(l1circuitrec)

    l1circKey = L1CircuitKey(l1PortAKey=l1portAkey, l1PortBKey=l1portBkey)
    l1circuitpathRec = L1CircuitPathRecord(l1CircKey=l1circKey, pathOption=1)
    l1circuitpathManager = plan.getNetwork().getL1Network().getL1CircuitPathManager()
    l1circuitpath = l1circuitpathManager.newL1CircuitPath(l1circuitpathRec)

    orderedl1hops = []
    orderedl1hops.append(l1nodeA)
    for l1hop in l1hops:
        for node in l1hop:
            if node == l1nodeA:
                pass
            elif not node in orderedl1hops:
                orderedl1hops.append(node)
    c = 0
    for l1hop in orderedl1hops:
        if l1hop == l1nodeA:
            hoptype = HopType('PathStrict', 0)
        else:
            hoptype = HopType('PathLoose', 0)
        l1hoprec = L1CircuitPathHopRecord(l1CircPathKey=l1circuitpath.getKey(), hopNode=L1NodeKey(l1hop),step=c,type=hoptype)
        l1circuitpath.addHop(l1hoprec)
        c += 1

    return l1circuit


def generateL3nodes(plan, l3nodelist):
    for l3node in l3nodelist:
        nodeRec = NodeRecord(name=l3node)
        plan.getNetwork().getNodeManager().newNode(nodeRec)


def generateL3circuit(plan,name,l3nodeA,l3nodeB):
    nodeAKey = NodeKey(l3nodeA)
    nodeBKey = NodeKey(l3nodeB)
    nodeAintfname = "L3_intf_" + name + "_to_"+ l3nodeB
    nodeBintfname = "L3_intf_" + name + "_to_"+ l3nodeA
    intfArec = InterfaceRecord(sourceKey=nodeAKey, name=nodeAintfname, isisLevel=2)
    intfBrec = InterfaceRecord(sourceKey=nodeBKey, name=nodeBintfname, isisLevel=2)
    circRec = CircuitRecord(name=name)
    network = plan.getNetwork()
    circuit = network.newConnection(ifaceARec=intfArec, ifaceBRec=intfBrec, circuitRec=circRec)

    return circuit