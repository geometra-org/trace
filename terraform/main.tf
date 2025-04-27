data "azurerm_resource_group" "pants_rg" {
  name = var.resource_group_name
}

resource "azurerm_container_app_environment" "remote_cache_env" {
  name                = "bazel-remote-environment"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_container_app" "bazel_app" {
  name                         = "bazel-remote-cache"
  container_app_environment_id = azurerm_container_app_environment.example.id
  resource_group_name          = azurerm_resource_group.example.name
  revision_mode                = "Single"

  template {
    container {
      name   = "bazel-remote-cache"
      image  = "buchgr/bazel-remote-cache:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
}
