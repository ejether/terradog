
resource "datadog_timeboard" "kubernetes_resource_timeboard" {
  title       = "Kubernetes Resource Timeboard"
  description = "Kubernetes Resource Timeboard"
  read_only   = false


  graph {
    title = "Node CPU Usage"
    viz   = "hostmap"
    request {
      q    = "sum:kubernetes.cpu.usage.total{$node,$kube_deployment} by {host}"
      type = "fill"
    }
  }

  graph {
    title = "Top CPU Pods"
    viz   = "toplist"
    request {
      q    = "top(sum:kubernetes.cpu.usage.total{$scope,$node,$kube_namespace,$kube_deployment} by {pod_name}, 10, 'mean', 'desc')"
      type = "None"
      style = {
        width   = "normal"
        palette = "warm"
        type    = "solid"
      }
    }
  }

  graph {
    title = "Top Pod CPU Utilitization"
    viz   = "timeseries"
    request {
      q          = "top(avg:docker.cpu.usage{$scope} by {pod_name}, 10, 'mean', 'desc')/avg:kubernetes.cpu.limits{$scope} by {pod_name}"
      type       = "line"
      aggregator = "avg"
      style = {
        width   = "normal"
        palette = "dog_classic"
        type    = "solid"
      }
    }
  }

  graph {
    title = "Node Mem Usage"
    viz   = "hostmap"
    request {
      q    = "sum:kubernetes.memory.usage{$node,$kube_deployment} by {host}"
      type = "fill"
    }
  }

  graph {
    title = "Sum of kubernetes.memory.usage over $scope,$node,$kube_namespace,$kube_deploy..."
    viz   = "toplist"
    request {
      q    = "top(sum:kubernetes.memory.usage{$scope,$node,$kube_namespace,$kube_deployment} by {pod_name}, 10, 'mean', 'desc')"
      type = "None"
      style = {
        width   = "normal"
        palette = "cool"
        type    = "solid"
      }
    }
  }

  graph {
    title = "Avg of kubernetes.memory.usage over $scope by pod_name"
    viz   = "timeseries"
    request {
      q          = "top(avg:kubernetes.memory.usage{$scope,$node,$kube_namespace,$kube_deployment} by {pod_name}, 10, 'mean', 'desc')/avg:kubernetes.memory.limits{$scope,$node,$kube_namespace,$kube_deployment} by {pod_name}*100"
      type       = "line"
      aggregator = "avg"
      style = {
        width   = "normal"
        palette = "dog_classic"
        type    = "solid"
      }
    }
  }

  template_variable {
    default = "*"
    name    = "scope"
    prefix  = "cluster_tag"
  }

  template_variable {
    default = "*"
    name    = "kube_namespace"
    prefix  = "kube_namespace"
  }

  template_variable {
    default = "*"
    name    = "kube_deployment"
    prefix  = "kube_deployment"
  }

  template_variable {
    default = "*"
    name    = "node"
    prefix  = "node"
  }

}
