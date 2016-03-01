#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from py2neo import Graph, Node, Relationship, watch
from py2neo.cypher.error.schema import ConstraintViolation


watch("httpstream")  #The watch function comes with the bundled httpstream library and simply dumps log entries to standard output.

graph = Graph("http://neo4j:080370053@localhost:7474/db/data/")
alice = Node("Person", name="Alice")
bob = Node("Person", name="Bob")
alice_knows_bob = Relationship(alice, "KNOWS", bob)
graph.create(alice_knows_bob)

graph.cypher.execute("CREATE (item:IP {ip:{ip},host:{host},time:{time}}) RETURN item", {"ip":"124.124", "host":"8800", "time":time.time()})

graph.schema.create_uniqueness_constraint("IP", "ip")


fmt_str = "{0} {1} {name} {2} {age}".format("welcome", "boy!", "...", name="owen", age=18)
print(fmt_str)