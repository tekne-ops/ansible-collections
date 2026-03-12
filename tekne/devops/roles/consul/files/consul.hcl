tls {
   defaults {
      ca_file = "<Consul configuration directory>/certs/consul-agent-ca.pem"
      cert_file = "<Consul configuration directory>/certs/dc1-server-consul-0.pem"
      key_file = "<Consul configuration directory>/certs/dc1-server-consul-0-key.pem"

      verify_incoming = true
      verify_outgoing = true

      domain = "consul.tekne.sv"
   }
   internal_rpc {
      verify_server_hostname = true
   }
}

auto_encrypt {
  allow_tls = true
}

acl {
  enabled = true
  default_policy = "deny"
  enable_token_persistence = true
}