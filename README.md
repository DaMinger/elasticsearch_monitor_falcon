# elasticsearch_monitor_falcon

希望有帮助，大家根据实际情况可以自定义修改。

## 集群级别

主要监控项 | 描述
---- | ----
es.cluster.health.active_primary_shards | 集群内所有索引的主分片总数
es.cluster.health.active_shards_percent_as_number | 可用分片百分比
es.cluster.health.alive | es是否能连接上
es.cluster.health.delayed_unassigned_shards | 延时待分配到具体节点上的分片数
es.cluster.health.initializing_shards | 正在初始化的分片数
es.cluster.health.number_of_data_nodes | 数据节点个数
es.cluster.health.number_of_nodes | 节点总个数
es.cluster.health.number_of_pending_tasks | 等待中任务的个数
es.cluster.health.relocating_shards | 正在迁移中的分片数
es.cluster.health.status | 集群健康状态
es.cluster.health.task_max_waiting_in_queue_millis | 任务在队列中等待的最长时间
es.cluster.health.unassigned_shards | 未分配到具体节点上的分片数

## 节点级别

主要监控项 | 描述
---- | ----
es.node.indices.flush.flush_latency | 每次flush操作的平均响应时间
es.node.indices.indexing.index_current | 当前indexing操作的个数
es.node.indices.indexing.indexing_latency | 每次indexing操作的平均响应时间
es.node.indices.refreshing.refresh_latency | 每次refreshing操作的平均响应时间
es.node.indices.search.fetch_current | 当前fetch操作的个数
es.node.indices.search.fetch_latency | 每次fetch操作的平均响应时间
es.node.indices.search.query_current | 当前query操作的个数
es.node.indices.search.query_latency | 每次query操作的平均响应时间
es.node.jvm.gc.collectors.heap_committed_in_bytes | Amount of JVM heap committed
es.node.jvm.gc.collectors.old.collection_count | old gc 发生的次数
es.node.jvm.gc.collectors.old.collection_time_latency | 每次old gc 时间
es.node.jvm.gc.collectors.young.collection_count | young gc 发生的次数
es.node.jvm.gc.collectors.young.collection_time_latency | 每次young gc的时间
es.node.jvm.mem.heap_used_percent | jvm heap使用内存的百分比
es.node.thread_pool.bulk.queue | 在队列里面的bulk操作个数
es.node.thread_pool.bulk.rejected | 拒绝掉的bulk操作个数
es.node.thread_pool.force_merge.queue | 在队列里面的force_merge操作个数
es.node.thread_pool.force_merge.rejected | 拒绝掉的force_merge操作个数
es.node.thread_pool.index.queue | 在队列里面的index操作个数
es.node.thread_pool.index.rejected | 拒绝掉的index操作个数
es.node.thread_pool.search.queue | 在队列里面的search操作个数
es.node.thread_pool.search.rejected | 拒绝掉的search操作个数
