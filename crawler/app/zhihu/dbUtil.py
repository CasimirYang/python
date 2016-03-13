#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import time
from py2neo import watch, Graph

from app.zhihu import User

watch("httpstream")  #The watch function comes with the bundled httpstream library and simply dumps log entries to standard output.
graph = Graph("http://neo4j:123456@localhost:7474/db/data/")
logger = logging.getLogger(__name__)

#graph.schema.create_uniqueness_constraint("IP", "ip")


def get_user():
    begin = time.time()
    statement = "match(user:user {have_disposed:'false'}) return user.user_id,user.user_name limit 10"
    record_list = graph.cypher.execute(statement)
    user_list = []
    for record in record_list:
        user_list.append(User(record[0], record[1], 'false'))
    end = time.time()
    #print("spent time:{0} to get users.".format(end-begin))
    logger.info("spent time:{0} to get users.".format(end-begin))
    return user_list


def save_user(user_list):
    begin = time.time()
    transaction = graph.cypher.begin()
    statement = "MERGE (peo:user{user_id:{user_id}}) ON MATCH SET peo.have_disposed={merge_disposed}  " \
                "ON CREATE SET peo.user_id={user_id},peo.user_name={user_name},peo.have_disposed={create_disposed}"
    # statement = "CREATE (:user {user_id:{user_id},user_name:{user_name},have_disposed:{have_disposed}})"
    for user in user_list:
        user_id = user.user_id
        user_name = user.user_name
        transaction.append(statement, {"user_id": user_id, "user_name": user_name, "merge_disposed": user.have_disposed, "create_disposed": user.have_disposed})
        transaction.process()
    transaction.commit()
    end = time.time()
    #print("spent time:{0} to save {1} users.".format(end-begin, len(user_list))) #todo
    logger.info("spent time:{0} to save {1} users.".format(end-begin, len(user_list)))


def save_followee(user, followee_list):
    begin = time.time()
    transaction = graph.cypher.begin()
    # statement = "MATCH (origin:user{user_id:{user_id}}),(followee:user{user_id:{followee_user_id}})" \
    #             " MERGE (origin)-[:follower]->(followee)"
    statement = "MATCH (origin:user{user_id:{user_id}}),(followee:user{user_id:{followee_user_id}})" \
                " MERGE (origin)-[:follower]->(followee)"
    for followee in followee_list:
        transaction.append(statement, {"user_id": user.user_id, "followee_user_id": followee.user_id})
        transaction.process()
    transaction.commit()
    end = time.time()
    logger.info("spent :{0} seconds to save {1} followees.".format(end-begin, len(followee_list)))


def save_follower(user, follower_list):
    begin = time.time()
    transaction = graph.cypher.begin()
    statement = "MATCH (follower:user {user_id:{follower_user_id}}),(origin:user {user_id:{user_id}})" \
                " MERGE (follower)-[:follower]->(origin)"
    for follower in follower_list:
        transaction.append(statement, {"follower_user_id": follower.user_id, "user_id": user.user_id})
        transaction.process()
    transaction.commit()
    end = time.time()
    logger.info("spent :{0} seconds to save {1} followers.".format(end-begin, len(follower_list)))
