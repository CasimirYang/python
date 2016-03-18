#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from py2neo import watch, Graph

from app.zhihu import User, log_time

# watch("httpstream")
graph = Graph("http://neo4j:123456@localhost:7474/db/data/")
logger = logging.getLogger(__name__)

#graph.schema.create_uniqueness_constraint("IP", "ip")


@log_time("get users.")
def get_user():
    statement = "MATCH(user:user {status:0}) RETURN user.user_id,user.user_name LIMIT 4"
    record_list = graph.cypher.execute(statement)
    user_list = []
    for record in record_list:
        user_list.append(User(record[0], record[1]))
    return user_list


@log_time("update users status.")
def update_user_status(user, status):
    statement = "MERGE (target:user {user_id:{user_id}}) SET target.user_name={user_name},target.status={status}"
    graph.cypher.execute(statement, {"user_id": user.user_id, "user_name": user.user_name, "status": status})


@log_time("save users.")
def save_user(user_list):
    transaction = graph.cypher.begin()
    statement = "MERGE (peo:user{user_id:{user_id}}) ON CREATE SET peo.user_name={user_name},peo.status={status}"
    for user in user_list:
        user_id = user.user_id
        user_name = user.user_name
        transaction.append(statement, {"user_id": user_id, "user_name": user_name, "status": user.status})
        transaction.process()
    transaction.commit()


@log_time("save follower relationship.")
def save_follow(user, followee_list, follow_type='ee'):
    transaction = graph.cypher.begin()
    statement = "MATCH (origin:user{user_id:{user_id}}),(followee:user{user_id:{followee_user_id}})" \
                " MERGE (origin)-[:follower]->(followee)"
    if follow_type == 'ee':
        follower = "user_id"
        followee = "followee_user_id"
    else:
        follower = "followee_user_id"
        followee = "user_id"

    for followee_item in followee_list:
        transaction.append(statement, {follower: user.user_id, followee: followee_item.user_id})
        transaction.process()
    transaction.commit()


@log_time("get total user.")
def get_total_user():
    statement = "MATCH (peo:user) RETURN COUNT(peo)"
    record = graph.cypher.execute(statement)[0]
    print("record:{0}".format(record[0]))
    return record[0]


@log_time("get total relationshiop.")
def get_total_relationshiop():
    statement = "MATCH (:user)-[relat:follower]->(:user) RETURN COUNT(relat)"
    record = graph.cypher.execute(statement)[0]
    print("record:{0}".format(record[0]))
    return record[0]