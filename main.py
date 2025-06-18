import json
import settings
from cluster.common import Setup_All_Nodes
from cluster.master import Setup_Cluster
from cluster.node import Join_Nodes
from cluster.cluster_status import Cluster_Status

servers = settings.servers

Setup_All_Nodes(servers)
Setup_Cluster(servers)
Join_Nodes(servers)
Cluster_Status(servers)