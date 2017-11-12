#!/bin/env python
#-*- coding:utf-8 -*-
#__author__ = 'DaMing'

from elasticsearch import *
import requests
import time
import json
import socket
import commands
import os
import sys

#获取本地连接
def getEsConn(hostname):
    es = Elasticsearch(hostname,request_timeout=25)
    return es

#定义falcon es监控列表
es_stat = []

#定义集群监控项
#health api
CLUSTER_HEALTH_KEYS = [
('status','GAUGE'),
('number_of_nodes','GAUGE'),
('unassigned_shards','GAUGE'),
('number_of_pending_tasks','GAUGE'),
('number_of_in_flight_fetch','GAUGE'),
('active_primary_shards','GAUGE'),
('task_max_waiting_in_queue_millis','GAUGE'),
('relocating_shards','GAUGE'),
('active_shards_percent_as_number','GAUGE'),
('initializing_shards','GAUGE'),
('number_of_data_nodes','GAUGE'),
('delayed_unassigned_shards','GAUGE'),
#es是否能连接上
('alive','GAUGE')
]

#node api
#indices api:search indexing refresh flush get warmer merges fielddata
INDICES_KEYS = [
('search.query_latency','GAUGE'),
('search.query_current','GAUGE'),
('search.fetch_latency','GAUGE'),
('search.fetch_current','GAUGE'),
('indexing.indexing_latency','GAUGE'),
('flush.flush_latency','GAUGE'),
('refresh.refresh_latency','GAUGE'),
('indexing.index_current','GAUGE'),
('get.current','GAUGE'),
('get.get_latency','GAUGE'),
('warmer.current','GAUGE'),
('warmer.warmer_latency','GAUGE'),
('merges.current','GAUGE'),
('merges.current_size_in_bytes','GAUGE'),
('merges.merges_latency','GAUGE'),
('fielddata.memory_size_in_bytes','GAUGE'),
('fielddata.evictions','GAUGE'),
('store.throttle_time_in_millis','GAUGE')
]
#jvm api
JVM_KEYS = [
('gc.collectors.young.collection_count','GAUGE'),
('gc.collectors.young.collection_time_latency','GAUGE'),
('gc.collectors.old.collection_count','GAUGE'),
('gc.collectors.old.collection_time_latency','GAUGE'),
('mem.heap_used_percent','GAUGE'),
('mem.heap_committed_in_bytes','GAUGE'),
('mem.heap_used_in_bytes','GAUGE'),
('mem.non_heap_used_in_bytes','GAUGE'),
('mem.non_heap_committed_in_bytes','GAUGE'),
('mem.pools.old.used_in_bytes','GAUGE'),
('mem.pools.old.peak_used_in_bytes','GAUGE'),
('mem.pools.old.used_percent','GAUGE'),
('threads.count','GAUGE'),
('threads.peak_count','GAUGE'),
('buffer_pools.direct.used_in_bytes','GAUGE'),
('buffer_pools.mapped.used_in_bytes','GAUGE')
]
#thread_pool api
THREAD_POOL_KEYS = [
('bulk.threads','GAUGE'),
('bulk.queue','GAUGE'),
('bulk.active','GAUGE'),
('bulk.rejected','GAUGE'),
('bulk.largest','GAUGE'),
('bulk.completed','GAUGE'),
('fetch_shard_started.threads','GAUGE'),
('fetch_shard_started.queue','GAUGE'),
('fetch_shard_started.active','GAUGE'),
('fetch_shard_started.rejected','GAUGE'),
('fetch_shard_started.largest','GAUGE'),
('fetch_shard_started.completed','GAUGE'),
('fetch_shard_store.threads','GAUGE'),
('fetch_shard_store.queue','GAUGE'),
('fetch_shard_store.active','GAUGE'),
('fetch_shard_store.rejected','GAUGE'),
('fetch_shard_store.largest','GAUGE'),
('fetch_shard_store.completed','GAUGE'),
('flush.threads','GAUGE'),
('flush.queue','GAUGE'),
('flush.active','GAUGE'),
('flush.rejected','GAUGE'),
('flush.largest','GAUGE'),
('flush.completed','GAUGE'),
('force_merge.threads','GAUGE'),
('force_merge.queue','GAUGE'),
('force_merge.active','GAUGE'),
('force_merge.rejected','GAUGE'),
('force_merge.largest','GAUGE'),
('force_merge.completed','GAUGE'),
('generic.threads','GAUGE'),
('generic.queue','GAUGE'),
('generic.active','GAUGE'),
('generic.rejected','GAUGE'),
('generic.largest','GAUGE'),
('generic.completed','GAUGE'),
('get.threads','GAUGE'),
('get.queue','GAUGE'),
('get.active','GAUGE'),
('get.rejected','GAUGE'),
('get.largest','GAUGE'),
('get.completed','GAUGE'),
('index.threads','GAUGE'),
('index.queue','GAUGE'),
('index.active','GAUGE'),
('index.rejected','GAUGE'),
('index.largest','GAUGE'),
('index.completed','GAUGE'),
('listener.threads','GAUGE'),
('listener.queue','GAUGE'),
('listener.active','GAUGE'),
('listener.rejected','GAUGE'),
('listener.largest','GAUGE'),
('listener.completed','GAUGE'),
('management.threads','GAUGE'),
('management.queue','GAUGE'),
('management.active','GAUGE'),
('management.rejected','GAUGE'),
('management.largest','GAUGE'),
('management.completed','GAUGE'),
('refresh.threads','GAUGE'),
('refresh.queue','GAUGE'),
('refresh.active','GAUGE'),
('refresh.rejected','GAUGE'),
('refresh.largest','GAUGE'),
('refresh.completed','GAUGE'),
('search.threads','GAUGE'),
('search.queue','GAUGE'),
('search.active','GAUGE'),
('search.rejected','GAUGE'),
('search.largest','GAUGE'),
('search.completed','GAUGE'),
('snapshot.threads','GAUGE'),
('snapshot.queue','GAUGE'),
('snapshot.active','GAUGE'),
('snapshot.rejected','GAUGE'),
('snapshot.largest','GAUGE'),
('snapshot.completed','GAUGE'),
('warmer.threads','GAUGE'),
('warmer.queue','GAUGE'),
('warmer.active','GAUGE'),
('warmer.rejected','GAUGE'),
('warmer.largest','GAUGE'),
('warmer.completed','GAUGE')
]

HTTP_KEYS = [
('http.current_open','GAUGE')
]

#
CLUSTER_NODE_KEYS = JVM_KEYS + THREAD_POOL_KEYS + INDICES_KEYS + HTTP_KEYS

def main():
    #获取主机名
    hostname = socket.gethostname().split("XXXX")[0]
    ip = socket.gethostbyname(hostname)
    #数据模型基本信息
    metric = 'es.cluster.health'
    endpoint = hostname
    timestamp = int(time.time())
    step = 60
    tags = ''
    try:
        es = getEsConn(hostname)
        cluster_health  = es.cluster.health()
        cluster_nodes = es.nodes.stats()
        tags = cluster_health['cluster_name']
    except Exception, e:
        key = 'alive'
        falcon_type = "GAUGE"
        value = 0
        falcon_format = {
            'metric': '%s.%s' % (metric, key),
            'endpoint': endpoint,
            'timestamp': timestamp,
            'step': step,
            'value': value,
            'counterType': falcon_type,
            'tags': tags
        }
        es_stat.append(falcon_format)
        print json.dumps(es_stat, sort_keys=True,indent=4)
        sys.exit(0)

    for key,falcon_type in CLUSTER_HEALTH_KEYS:
        if key == 'status':
            if cluster_health['status'] == "green":
                value = 2
            elif cluster_health['status'] == "yellow":
                value = 1
            elif cluster_health['status'] == "red":
                vaule = 0
        elif key == 'alive':
            value = 1
        else:
            try:
                value = int(cluster_health[key])
            except:
                continue
        falcon_format = {
                'metric': '%s.%s' % (metric, key),
                'endpoint': endpoint,
                'timestamp': timestamp,
                'step': step,
                'value': value,
                'counterType': falcon_type,
                'tags': tags
            }
        es_stat.append(falcon_format)
    #print json.dumps(es_stat, sort_keys=True,indent=4)

    for key,falcon_type in CLUSTER_NODE_KEYS:
        for node_stats in cluster_nodes['nodes']:
            if ip == cluster_nodes['nodes'][node_stats]['host']:
                tags = cluster_nodes['nodes'][node_stats]['name']
                element = (key,falcon_type)
                if element in JVM_KEYS:
                    metric = 'es.node.jvm'
                    if key == 'gc.collectors.young.collection_time_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['jvm']['gc']['collectors']['young']['collection_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['jvm']['gc']['collectors']['young']['collection_count'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'gc.collectors.old.collection_time_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['jvm']['gc']['collectors']['old']['collection_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['jvm']['gc']['collectors']['old']['collection_count'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'mem.pools.old.used_percent':
                        try:
                            value = float(cluster_nodes['nodes'][node_stats]['jvm']['mem']['pools']['old']['used_in_bytes'])/int(cluster_nodes['nodes'][node_stats]['jvm']['mem']['pools']['old']['max_in_bytes'])*100
                        except ZeroDivisionError:
                            value = 0
                    elif len(key.split('.')) == 2:
                        value = int(cluster_nodes['nodes'][node_stats]['jvm']['%s' %(key.split('.')[0])]['%s' %(key.split('.')[1])])
                    elif len(key.split('.')) == 4:
                        value = int(cluster_nodes['nodes'][node_stats]['jvm']['%s' %(key.split('.')[0])]['%s' %(key.split('.')[1])]['%s' %(key.split('.')[2])]['%s' %(key.split('.')[3])])
                elif element in THREAD_POOL_KEYS:
                    metric = 'es.node.thread_pool'
                    value = int(cluster_nodes['nodes'][node_stats]['thread_pool']['%s' %(key.split('.')[0])]['%s' %(key.split('.')[1])])
                elif element in INDICES_KEYS:
                    metric = 'es.node.indices'
                    if key == 'search.query_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['search']['query_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['search']['query_total'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'search.fetch_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['search']['fetch_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['search']['fetch_total'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'indexing.indexing_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['indexing']['index_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['indexing']['index_total'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'flush.flush_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['flush']['total_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['flush']['total'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'refresh.refresh_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['refresh']['total_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['refresh']['total'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'get.get_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['get']['time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['get']['total'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'warmer.warmer_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['warmer']['total_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['warmer']['total'])
                        except ZeroDivisionError:
                            value = 0
                    elif key == 'merges.merges_latency':
                        try:
                            value = int(cluster_nodes['nodes'][node_stats]['indices']['merges']['total_time_in_millis'])/int(cluster_nodes['nodes'][node_stats]['indices']['merges']['total'])
                        except ZeroDivisionError:
                            value = 0
                    elif len(key.split('.')) == 2:
                        value = int(cluster_nodes['nodes'][node_stats]['indices']['%s' %(key.split('.')[0])]['%s' %(key.split('.')[1])])
                elif element in HTTP_KEYS:
                    metric = 'es.node'
                    value = int(cluster_nodes['nodes'][node_stats]['%s' %(key.split('.')[0])]['%s' %(key.split('.')[1])])

                falcon_format = {
                    'metric': '%s.%s' % (metric, key),
                    'endpoint': endpoint,
                    'timestamp': timestamp,
                    'step': step,
                    'value': value,
                    'counterType': falcon_type,
                    'tags': 'node=%s' % (tags)
                }
                es_stat.append(falcon_format)
    print json.dumps(es_stat, sort_keys=True,indent=4)

if __name__ == '__main__':
    proc = commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' % os.path.basename(sys.argv[0]))
    if int(proc) < 5:
        main()
