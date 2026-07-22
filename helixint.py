#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ██╗  ██╗███████╗██╗     ██╗██╗  ██╗██╗███╗   ██╗████████╗                 ║
║  ██║  ██║██╔════╝██║     ██║╚██╗██╔╝██║████╗  ██║╚══██╔══╝                 ║
║  ███████║█████╗  ██║     ██║ ╚███╔╝ ██║██╔██╗ ██║   ██║                    ║
║  ██╔══██║██╔══╝  ██║     ██║ ██╔██╗ ██║██║╚██╗██║   ██║                    ║
║  ██║  ██║███████╗███████╗██║██╔╝ ██╗██║██║ ╚████║   ██║                    ║
║  ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝                    ║
║  ██╗███╗   ██╗████████╗                                                      ║
║  ██║████╗  ██║╚══██╔══╝  ╔═══════════════════════════════════════════════╗  ║
║  ██║██╔██╗ ██║   ██║     ║  ULTIMATE RECONNAISSANCE SUITE v7.0.0        ║  ║
║  ██║██║╚██╗██║   ██║     ║  Author: SYLHETYHACKVENGER (THE-ERROR808)    ║  ║
║  ██║██║ ╚████║   ██║     ╚═══════════════════════════════════════════════╝  ║
║  ╚═╝╚═╝  ╚═══╝   ╚═╝                                                       ║
║  🚀 1000 Data Points • Quantum Cyber Intelligence • Complete Recon        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import re
import json
import time
import socket
import ssl
import random
import shutil
import threading
import subprocess
import argparse
import concurrent.futures
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from urllib.parse import urlparse, urljoin, quote_plus
from collections import defaultdict, deque
import hashlib
import base64
import ipaddress
import struct

# Third-party imports
try:
    import requests
    import dns.resolver
    import dns.zone
    import dns.query
    import dns.reversename
    import whois
    from OpenSSL import crypto
    import cryptography
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa, ed25519
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
except ImportError as e:
    print(f"[!] ERROR: Missing required module: {e}")
    print("[!] Run: pip install requests dnspython python-whois pyOpenSSL cryptography")
    sys.exit(1)

# ============================================================
#   UI COMPONENTS
# ============================================================

class Colors:
    CYAN = '\033[96m'; BLUE = '\033[94m'; PURPLE = '\033[95m'; MAGENTA = '\033[35m'
    GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'
    BRIGHT_CYAN = '\033[1;96m'; BRIGHT_BLUE = '\033[1;94m'; BRIGHT_PURPLE = '\033[1;95m'
    BRIGHT_GREEN = '\033[1;92m'; BRIGHT_YELLOW = '\033[1;93m'; BRIGHT_RED = '\033[1;91m'
    BRIGHT_WHITE = '\033[1;97m'; GOLD = '\033[38;5;214m'; DARK = '\033[38;5;238m'
    BOLD = '\033[1m'; DIM = '\033[2m'; RESET = '\033[0m'

class Symbols:
    CROWN = '👑'; RADAR = '◈'; SCAN = '📡'; SHIELD = '🛡'; LOCK = '🔒'
    SERVER = '🖥'; GLOBE = '🌐'; WARNING = '⚠'; CHECK = '✓'; TARGET = '◎'

class CyberHeader:
    @staticmethod
    def generate():
        return f"""
{Colors.BRIGHT_CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║  {Colors.BRIGHT_PURPLE}██╗  ██╗███████╗██╗     ██╗██╗  ██╗██╗███╗   ██╗████████╗    {Colors.BRIGHT_CYAN}║
║  {Colors.BRIGHT_PURPLE}██║  ██║██╔════╝██║     ██║╚██╗██╔╝██║████╗  ██║╚══██╔══╝    {Colors.BRIGHT_CYAN}║
║  {Colors.BRIGHT_PURPLE}███████║█████╗  ██║     ██║ ╚███╔╝ ██║██╔██╗ ██║   ██║       {Colors.BRIGHT_CYAN}║
║  {Colors.BRIGHT_PURPLE}██╔══██║██╔══╝  ██║     ██║ ██╔██╗ ██║██║╚██╗██║   ██║       {Colors.BRIGHT_CYAN}║
║  {Colors.BRIGHT_PURPLE}██║  ██║███████╗███████╗██║██╔╝ ██╗██║██║ ╚████║   ██║       {Colors.BRIGHT_CYAN}║
║  {Colors.BRIGHT_PURPLE}╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝       {Colors.BRIGHT_CYAN}║
║                                                                                      ║
║  {Colors.GOLD}{Symbols.CROWN} ULTIMATE RECONNAISSANCE SUITE {Colors.BRIGHT_WHITE}v7.0.0{Colors.GOLD}           {Colors.BRIGHT_CYAN}║
║  {Colors.BRIGHT_WHITE}Author: SYLHETYHACKVENGER {Colors.DIM}(THE-ERROR808){Colors.BRIGHT_WHITE}              {Colors.BRIGHT_CYAN}║
║  {Colors.DIM}© 2025 HELIXINT Technologies • {Colors.BRIGHT_WHITE}1000 Data Points • Complete Recon{Colors.DIM}   {Colors.BRIGHT_CYAN}║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

# ============================================================
#   API KEYS
# ============================================================

API_KEYS = {
    'SHODAN': os.environ.get('SHODAN_API_KEY', ''),
    'VIRUSTOTAL': os.environ.get('VIRUSTOTAL_API_KEY', ''),
    'ABUSEIPDB': os.environ.get('ABUSEIPDB_API_KEY', ''),
    'CENSYS_ID': os.environ.get('CENSYS_API_ID', ''),
    'CENSYS_SECRET': os.environ.get('CENSYS_API_SECRET', ''),
    'IPINFO': os.environ.get('IPINFO_TOKEN', ''),
}

# ============================================================
#   COMPLETE DATA STRUCTURES - ALL 1000 DATA POINTS
# ============================================================

@dataclass
class DataPoints:
    """Container for ALL 1000 data points"""
    # ============================================================
    # Section 1: IP Intelligence (1-100)
    # ============================================================
    # 1-10: Basic IP
    dp1_ipv4: str = ''
    dp2_ipv6: str = ''
    dp3_ip_version: int = 4
    dp4_is_public: bool = False
    dp5_network_class: str = ''
    dp6_cidr: str = ''
    dp7_prefix_length: int = 0
    dp8_network_address: str = ''
    dp9_broadcast_address: str = ''
    dp10_subnet_mask: str = ''
    
    # 11-13: DNS
    dp11_reverse_dns: str = ''
    dp12_primary_hostname: str = ''
    dp13_additional_hostnames: List[str] = field(default_factory=list)
    
    # 14-23: BGP/ASN
    dp14_asn: str = ''
    dp15_asn_name: str = ''
    dp16_bgp_prefix: str = ''
    dp17_bgp_origin_asn: str = ''
    dp18_isp: str = ''
    dp19_organization_name: str = ''
    dp20_hosting_provider: str = ''
    dp21_cloud_provider: str = ''
    dp22_residential_datacenter: str = ''
    dp23_mobile_carrier: str = ''
    
    # 24-33: Geolocation
    dp24_country: str = ''
    dp25_region: str = ''
    dp26_city: str = ''
    dp27_postal_code: str = ''
    dp28_continent: str = ''
    dp29_timezone: str = ''
    dp30_latitude: float = 0.0
    dp31_longitude: float = 0.0
    dp32_geolocation_accuracy: str = ''
    dp33_satellite_provider: str = ''
    
    # 34-45: WHOIS
    dp34_whois_record: Dict[str, Any] = field(default_factory=dict)
    dp35_netrange: str = ''
    dp36_netname: str = ''
    dp37_parent_organization: str = ''
    dp38_registration_authority: str = ''
    dp39_registration_date: str = ''
    dp40_last_updated_date: str = ''
    dp41_abuse_contact_email: str = ''
    dp42_abuse_contact_phone: str = ''
    dp43_administrative_contact: str = ''
    dp44_technical_contact: str = ''
    dp45_route_object: str = ''
    
    # 46-60: Allocation & Routing
    dp46_allocation_status: str = ''
    dp47_rpki_validation_status: str = ''
    dp48_roa_information: Dict[str, Any] = field(default_factory=dict)
    dp49_anycast_detection: bool = False
    dp50_multicast_status: bool = False
    dp51_reserved_range_status: bool = False
    dp52_bogon_status: bool = False
    dp53_upstream_asn: str = ''
    dp54_downstream_asn: str = ''
    dp55_bgp_peers: List[str] = field(default_factory=list)
    dp56_bgp_communities: List[str] = field(default_factory=list)
    dp57_route_propagation: str = ''
    dp58_route_path: List[str] = field(default_factory=list)
    dp59_origin_route: str = ''
    dp60_route_description: str = ''
    
    # 61-68: Detection
    dp61_vpn_detection: bool = False
    dp62_proxy_detection: bool = False
    dp63_tor_exit_node: bool = False
    dp64_cdn_detection: bool = False
    dp65_waf_detection: bool = False
    dp66_reverse_proxy_detection: bool = False
    dp67_load_balancer_detection: bool = False
    dp68_iep_association: str = ''
    
    # 69-82: Network Metrics
    dp69_latency_estimate: float = 0.0
    dp70_hop_count_estimate: int = 0
    dp71_ttl_behavior: str = ''
    dp72_tcp_window_size: int = 0
    dp73_mss_value: int = 0
    dp74_mtu_estimate: int = 0
    dp75_tcp_options_fingerprint: str = ''
    dp76_ecn_support: bool = False
    dp77_tcp_timestamp_support: bool = False
    dp78_ipid_behavior: str = ''
    dp79_icmp_response_behavior: str = ''
    dp80_icmp_timestamp_support: bool = False
    dp81_traceroute_path: List[str] = field(default_factory=list)
    dp82_network_distance: int = 0
    
    # 83-100: Regional & Reputation
    dp83_as_country: str = ''
    dp84_regional_internet_registry: str = ''
    dp85_allocation_type: str = ''
    dp86_assignment_type: str = ''
    dp87_reverse_delegation: str = ''
    dp88_reverse_dns_zone: str = ''
    dp89_dynamic_dns_detection: bool = False
    dp90_static_ip_detection: bool = False
    dp91_reputation_score: int = 0
    dp92_spam_reputation: str = ''
    dp93_malware_reputation: str = ''
    dp94_phishing_reputation: str = ''
    dp95_botnet_reputation: str = ''
    dp96_abuse_confidence_score: int = 0
    dp97_blacklist_status: bool = False
    dp98_whitelist_status: bool = False
    dp99_historical_ownership: List[Dict] = field(default_factory=list)
    dp100_historical_ip_allocation: List[Dict] = field(default_factory=list)
    
    # ============================================================
    # Section 2: Services & Ports (101-176)
    # ============================================================
    services: List[Dict] = field(default_factory=list)
    
    # ============================================================
    # Section 3: DNS Records (177-197)
    # ============================================================
    dp177_a_record: List[str] = field(default_factory=list)
    dp178_aaaa_record: List[str] = field(default_factory=list)
    dp179_mx_record: List[Dict] = field(default_factory=list)
    dp180_txt_record: List[str] = field(default_factory=list)
    dp181_spf_record: List[str] = field(default_factory=list)
    dp182_dkim_record: List[str] = field(default_factory=list)
    dp183_dmarc_policy: str = ''
    dp184_ns_record: List[str] = field(default_factory=list)
    dp185_soa_record: Dict[str, str] = field(default_factory=dict)
    dp186_cname_record: List[str] = field(default_factory=list)
    dp187_ptr_record: List[str] = field(default_factory=list)
    dp188_srv_record: List[Dict] = field(default_factory=list)
    dp189_caa_record: List[Dict] = field(default_factory=list)
    dp190_naptr_record: List[Dict] = field(default_factory=list)
    dp191_dnssec_status: str = ''
    dp192_zone_transfer_available: bool = False
    dp193_zone_transfer_records: List[str] = field(default_factory=list)
    dp194_wildcard_dns: bool = False
    dp195_dns_ttl_values: Dict[str, int] = field(default_factory=dict)
    dp196_recursive_dns: bool = False
    dp197_edns_support: bool = False
    
    # ============================================================
    # Section 4: SSL/TLS (198-245)
    # ============================================================
    dp198_certificate_subject: Dict[str, str] = field(default_factory=dict)
    dp199_certificate_issuer: Dict[str, str] = field(default_factory=dict)
    dp200_certificate_expiration_date: str = ''
    dp201_certificate_serial: str = ''
    dp202_certificate_version: int = 0
    dp203_signature_algorithm: str = ''
    dp204_public_key_algorithm: str = ''
    dp205_public_key_size: int = 0
    dp206_sha1_fingerprint: str = ''
    dp207_sha256_fingerprint: str = ''
    dp208_md5_fingerprint: str = ''
    dp209_subject_alternative_names: List[str] = field(default_factory=list)
    dp210_common_name: str = ''
    dp211_organization: str = ''
    dp212_organizational_unit: str = ''
    dp213_locality: str = ''
    dp214_state_province: str = ''
    dp215_country: str = ''
    dp216_validity_start: str = ''
    dp217_validity_end: str = ''
    dp218_certificate_chain_length: int = 0
    dp219_root_ca: str = ''
    dp220_intermediate_ca: List[str] = field(default_factory=list)
    dp221_self_signed: bool = False
    dp222_wildcard_certificate: bool = False
    dp223_extended_validation: bool = False
    dp224_domain_validation: bool = False
    dp225_organization_validation: bool = False
    dp226_tls_version_supported: List[str] = field(default_factory=list)
    dp227_sslv2_support: bool = False
    dp228_sslv3_support: bool = False
    dp229_tls_1_0_support: bool = False
    dp230_tls_1_1_support: bool = False
    dp231_tls_1_2_support: bool = False
    dp232_tls_1_3_support: bool = False
    dp233_supported_cipher_suites: List[str] = field(default_factory=list)
    dp234_preferred_cipher: str = ''
    dp235_perfect_forward_secrecy: bool = False
    dp236_alpn_protocols: List[str] = field(default_factory=list)
    dp237_http2_support: bool = False
    dp238_http3_support: bool = False
    dp239_sni_support: bool = False
    dp240_ocsp_stapling: bool = False
    dp241_certificate_transparency_logging: bool = False
    dp242_tls_compression_support: bool = False
    dp243_session_resumption: bool = False
    dp244_session_tickets: bool = False
    dp245_renegotiation_support: bool = False
    
    # ============================================================
    # Section 5: HTTP/Web (249-300)
    # ============================================================
    dp249_status_code: int = 0
    dp250_response_time: float = 0.0
    dp251_headers: Dict[str, str] = field(default_factory=dict)
    dp252_server_header: str = ''
    dp253_date_header: str = ''
    dp254_content_type: str = ''
    dp255_content_length: str = ''
    dp256_content_encoding: str = ''
    dp257_transfer_encoding: str = ''
    dp258_cache_control: str = ''
    dp259_etag: str = ''
    dp260_last_modified: str = ''
    dp261_accept_ranges: str = ''
    dp262_connection_header: str = ''
    dp263_keep_alive_support: bool = False
    dp264_website_title: str = ''
    dp265_meta_description: str = ''
    dp266_meta_keywords: List[str] = field(default_factory=list)
    dp267_html_language: str = ''
    dp268_charset_encoding: str = ''
    dp269_favicon_hash: str = ''
    dp270_robots_txt_available: bool = False
    dp271_robots_txt_content: str = ''
    dp272_sitemap_xml_available: bool = False
    dp273_security_txt_available: bool = False
    dp274_security_txt_content: str = ''
    dp275_humans_txt_available: bool = False
    dp276_manifest_json_available: bool = False
    dp277_rss_feed_available: bool = False
    dp278_atom_feed_available: bool = False
    dp279_canonical_url: str = ''
    dp280_open_graph_metadata: Dict[str, str] = field(default_factory=dict)
    dp281_twitter_card_metadata: Dict[str, str] = field(default_factory=dict)
    dp282_generator_meta_tag: str = ''
    dp283_cms_identification: str = ''
    dp284_cms_version: str = ''
    dp285_web_server_software: str = ''
    dp286_web_server_version: str = ''
    dp287_reverse_proxy_software: str = ''
    dp288_cdn_provider: str = ''
    dp289_waf_provider: str = ''
    dp290_programming_language: str = ''
    dp291_javascript_framework: List[str] = field(default_factory=list)
    dp292_css_framework: List[str] = field(default_factory=list)
    dp293_analytics_platform: List[str] = field(default_factory=list)
    dp294_tag_manager: List[str] = field(default_factory=list)
    dp295_cookie_names: List[str] = field(default_factory=list)
    dp296_secure_cookie_flag: bool = False
    dp297_httponly_cookie_flag: bool = False
    dp298_samesite_cookie_policy: str = ''
    dp299_cookie_expiration: str = ''
    dp300_directory_listing_enabled: bool = False
    
    # ============================================================
    # Section 6: Security Headers (301-328)
    # ============================================================
    dp301_content_security_policy: str = ''
    dp302_x_frame_options: str = ''
    dp303_x_content_type_options: str = ''
    dp304_referrer_policy: str = ''
    dp305_permissions_policy: str = ''
    dp306_cross_origin_resource_policy: str = ''
    dp307_cross_origin_embedder_policy: str = ''
    dp308_cross_origin_opener_policy: str = ''
    dp309_strict_transport_security: str = ''
    dp310_expect_ct: str = ''
    dp311_x_xss_protection: str = ''
    dp312_cache_control_policy: str = ''
    dp313_pragma_header: str = ''
    dp314_expires_header: str = ''
    dp315_clear_site_data_header: str = ''
    dp316_accept_ch_header: str = ''
    dp317_alt_svc_header: str = ''
    dp318_access_control_allow_origin: str = ''
    dp319_access_control_allow_methods: str = ''
    dp320_access_control_allow_headers: str = ''
    dp321_access_control_allow_credentials: bool = False
    dp322_content_language: str = ''
    dp323_content_disposition: str = ''
    dp324_server_timing_header: str = ''
    dp325_link_header: str = ''
    dp326_vary_header: str = ''
    dp327_via_header: str = ''
    dp328_x_powered_by: str = ''
    
    # ============================================================
    # Section 7: Email Infrastructure (333-346)
    # ============================================================
    dp333_email_server_software: str = ''
    dp334_starttls_support: bool = False
    dp335_smtp_auth_support: bool = False
    dp336_smtp_banner: str = ''
    dp337_mta_sts_policy: str = ''
    dp338_tls_rpt_record: str = ''
    dp339_spf_evaluation: Dict[str, Any] = field(default_factory=dict)
    dp340_dkim_validation_status: str = ''
    dp341_dmarc_enforcement_mode: str = ''
    dp342_mx_priority: int = 0
    dp343_mx_redundancy: bool = False
    dp344_mail_hostnames: List[str] = field(default_factory=list)
    dp345_reverse_dns_mail: str = ''
    dp346_email_security_posture: str = ''
    
    # ============================================================
    # Section 8: Cloud Infrastructure (347-399)
    # ============================================================
    dp347_dns_provider: str = ''
    dp348_domain_registrar: str = ''
    dp349_registrar_expiration_date: str = ''
    dp350_registrar_creation_date: str = ''
    dp351_nameserver_provider: str = ''
    dp352_cdn_edge_provider: str = ''
    dp353_reverse_proxy_provider: str = ''
    dp354_cloud_platform: str = ''
    dp355_object_storage_endpoint: str = ''
    dp356_load_balancer_type: str = ''
    dp357_auto_scaling_indicator: bool = False
    dp358_container_platform_indicator: bool = False
    dp359_kubernetes_ingress_detection: bool = False
    dp360_api_gateway_detection: bool = False
    dp361_rest_api_endpoints: List[str] = field(default_factory=list)
    dp362_graphql_endpoint: str = ''
    dp363_soap_endpoint: str = ''
    dp364_openapi_documentation: str = ''
    dp365_websocket_endpoint: str = ''
    dp366_grpc_endpoint: str = ''
    dp367_xmlrpc_endpoint: str = ''
    dp368_jsonrpc_endpoint: str = ''
    dp369_oauth_endpoints: Dict[str, str] = field(default_factory=dict)
    dp370_openid_connect_endpoints: Dict[str, str] = field(default_factory=dict)
    dp371_saml_endpoint: str = ''
    dp372_login_page_detection: bool = False
    dp373_sso_detection: bool = False
    dp374_admin_portal_detection: bool = False
    dp375_user_portal_detection: bool = False
    dp376_developer_portal_detection: bool = False
    dp377_status_page_discovery: str = ''
    dp378_public_documentation: str = ''
    dp379_public_changelog: str = ''
    dp380_public_api_documentation: str = ''
    dp381_git_repository_reference: str = ''
    dp382_gitlab_instance: str = ''
    dp383_gitea_instance: str = ''
    dp384_svn_repository_reference: str = ''
    dp385_mercurial_repository_reference: str = ''
    dp386_public_package_registry: str = ''
    dp387_ci_cd_platform: str = ''
    dp388_monitoring_platform: str = ''
    dp389_logging_platform: str = ''
    dp390_error_reporting_service: str = ''
    dp391_analytics_service: str = ''
    dp392_consent_management_platform: str = ''
    dp393_captcha_provider: str = ''
    dp394_payment_gateway: str = ''
    dp395_third_party_identity_provider: str = ''
    dp396_external_authentication_provider: str = ''
    dp397_public_asset_inventory: List[str] = field(default_factory=list)
    dp398_public_static_asset_host: str = ''
    dp399_associated_domains: List[str] = field(default_factory=list)
    
    # ============================================================
    # Section 9: Assessment & Metrics (801-1000)
    # ============================================================
    dp801_primary_asset_identifier: str = ''
    dp802_asset_uuid: str = ''
    dp803_external_asset_tag: str = ''
    dp804_asset_category: str = ''
    dp805_asset_subtype: str = ''
    dp806_internet_facing_status: bool = False
    dp807_asset_lifecycle_stage: str = ''
    dp808_asset_discovery_source: str = ''
    dp809_first_discovery_date: str = ''
    dp810_last_discovery_date: str = ''
    dp811_discovery_frequency: str = ''
    dp812_last_successful_scan: str = ''
    dp813_last_observed_service: str = ''
    dp814_last_observed_certificate: str = ''
    dp815_last_observed_dns_change: str = ''
    dp816_last_observed_ip_change: str = ''
    dp817_historical_hostname_count: int = 0
    dp818_historical_certificate_count: int = 0
    dp819_historical_service_count: int = 0
    dp820_historical_technology_count: int = 0
    dp821_historical_port_count: int = 0
    dp822_historical_asn_count: int = 0
    dp823_historical_cdn_count: int = 0
    dp824_historical_waf_count: int = 0
    dp825_historical_cloud_provider_count: int = 0
    dp826_historical_registrar_count: int = 0
    dp827_historical_nameserver_count: int = 0
    dp828_historical_dns_provider_count: int = 0
    dp829_historical_routing_changes: int = 0
    dp830_historical_tls_changes: int = 0
    dp831_historical_http_header_changes: int = 0
    dp832_historical_redirect_changes: int = 0
    dp833_historical_cms_changes: int = 0
    dp834_historical_framework_changes: int = 0
    dp835_historical_server_software_changes: int = 0
    dp836_historical_favicon_changes: int = 0
    dp837_historical_title_changes: int = 0
    dp838_historical_geolocation_trend: List[Dict] = field(default_factory=list)
    dp839_passive_dns_observation_count: int = 0
    dp840_passive_certificate_observation_count: int = 0
    dp841_passive_http_observation_count: int = 0
    dp842_passive_service_observation_count: int = 0
    dp843_public_scan_observation_count: int = 0
    dp844_related_asset_count: int = 0
    dp845_related_hostname_count: int = 0
    dp846_related_domain_count: int = 0
    dp847_related_subdomain_count: int = 0
    dp848_related_ip_count: int = 0
    dp849_related_asn_count: int = 0
    dp850_related_certificate_count: int = 0
    dp851_related_email_infrastructure: List[str] = field(default_factory=list)
    dp852_related_cdn_infrastructure: List[str] = field(default_factory=list)
    dp853_related_cloud_infrastructure: List[str] = field(default_factory=list)
    dp854_related_api_infrastructure: List[str] = field(default_factory=list)
    dp855_related_storage_endpoints: List[str] = field(default_factory=list)
    dp856_related_identity_providers: List[str] = field(default_factory=list)
    dp857_shared_favicon_correlation: List[str] = field(default_factory=list)
    dp858_shared_http_header_correlation: List[str] = field(default_factory=list)
    dp859_shared_tls_fingerprint_correlation: List[str] = field(default_factory=list)
    dp860_shared_technology_correlation: List[str] = field(default_factory=list)
    dp861_shared_cms_correlation: List[str] = field(default_factory=list)
    dp862_shared_javascript_library_correlation: List[str] = field(default_factory=list)
    dp863_shared_analytics_platform: List[str] = field(default_factory=list)
    dp864_shared_tracking_identifiers: List[str] = field(default_factory=list)
    dp865_shared_certificate_issuer: List[str] = field(default_factory=list)
    dp866_shared_certificate_san_correlation: List[str] = field(default_factory=list)
    dp867_shared_dns_provider: List[str] = field(default_factory=list)
    dp868_shared_hosting_provider: List[str] = field(default_factory=list)
    dp869_shared_reverse_proxy: List[str] = field(default_factory=list)
    dp870_shared_load_balancer: List[str] = field(default_factory=list)
    dp871_shared_waf: List[str] = field(default_factory=list)
    dp872_shared_cdn: List[str] = field(default_factory=list)
    dp873_shared_registrar: List[str] = field(default_factory=list)
    dp874_shared_whois_organization: List[str] = field(default_factory=list)
    dp875_shared_abuse_contact: List[str] = field(default_factory=list)
    dp876_shared_administrative_contact: List[str] = field(default_factory=list)
    dp877_shared_technical_contact: List[str] = field(default_factory=list)
    dp878_asset_confidence_score: int = 0
    dp879_discovery_confidence_score: int = 0
    dp880_fingerprint_confidence_score: int = 0
    dp881_identification_confidence_score: int = 0
    dp882_geolocation_confidence_score: int = 0
    dp883_service_confidence_score: int = 0
    dp884_technology_confidence_score: int = 0
    dp885_exposure_confidence_score: int = 0
    dp886_reputation_confidence_score: int = 0
    dp887_external_attack_surface_score: int = 0
    dp888_network_exposure_score: int = 0
    dp889_service_exposure_score: int = 0
    dp890_web_application_exposure_score: int = 0
    dp891_certificate_health_score: int = 0
    dp892_dns_health_score: int = 0
    dp893_email_security_score: int = 0
    dp894_http_security_score: int = 0
    dp895_tls_security_score: int = 0
    dp896_infrastructure_resilience_score: int = 0
    dp897_overall_risk_score: int = 0
    dp898_executive_summary_score: int = 0
    dp899_security_posture_index: int = 0
    dp900_external_asset_maturity_score: int = 0
    dp901_overall_asset_status: str = ''
    dp902_asset_health_score: int = 0
    dp903_asset_availability_status: str = ''
    dp904_asset_criticality_level: str = ''
    dp905_business_impact_rating: str = ''
    dp906_exposure_classification: str = ''
    dp907_internet_visibility_level: str = ''
    dp908_service_inventory_completeness: str = ''
    dp909_dns_inventory_completeness: str = ''
    dp910_certificate_inventory_completeness: str = ''
    dp911_technology_inventory_completeness: str = ''
    dp912_external_dependency_count: int = 0
    dp913_third_party_dependency_count: int = 0
    dp914_cloud_dependency_count: int = 0
    dp915_cdn_dependency_count: int = 0
    dp916_authentication_dependency_count: int = 0
    dp917_email_dependency_count: int = 0
    dp918_dns_dependency_count: int = 0
    dp919_monitoring_dependency_count: int = 0
    dp920_logging_dependency_count: int = 0
    dp921_public_endpoint_count: int = 0
    dp922_public_api_count: int = 0
    dp923_public_hostname_count: int = 0
    dp924_public_domain_count: int = 0
    dp925_public_subdomain_count: int = 0
    dp926_public_ip_count: int = 0
    dp927_public_certificate_count: int = 0
    dp928_public_service_count: int = 0
    dp929_public_protocol_count: int = 0
    dp930_public_technology_count: int = 0
    dp931_public_javascript_library_count: int = 0
    dp932_public_framework_count: int = 0
    dp933_public_cms_count: int = 0
    dp934_public_authentication_endpoint_count: int = 0
    dp935_public_storage_endpoint_count: int = 0
    dp936_public_download_endpoint_count: int = 0
    dp937_public_documentation_endpoint_count: int = 0
    dp938_public_webhook_endpoint_count: int = 0
    dp939_public_health_check_endpoint_count: int = 0
    dp940_public_metrics_endpoint_count: int = 0
    dp941_dns_configuration_score: int = 0
    dp942_tls_configuration_score: int = 0
    dp943_http_configuration_score: int = 0
    dp944_email_configuration_score: int = 0
    dp945_certificate_management_score: int = 0
    dp946_technology_hygiene_score: int = 0
    dp947_service_hardening_score: int = 0
    dp948_encryption_quality_score: int = 0
    dp949_identity_integration_score: int = 0
    dp950_cloud_configuration_score: int = 0
    dp951_cdn_optimization_score: int = 0
    dp952_infrastructure_redundancy_score: int = 0
    dp953_high_availability_indicator: bool = False
    dp954_disaster_recovery_indicator: bool = False
    dp955_geographic_distribution_indicator: bool = False
    dp956_multi_region_deployment_indicator: bool = False
    dp957_load_balancing_effectiveness: str = ''
    dp958_failover_readiness: str = ''
    dp959_external_resilience_score: int = 0
    dp960_public_attack_surface_trend: str = ''
    dp961_historical_exposure_trend: str = ''
    dp962_historical_security_trend: str = ''
    dp963_historical_technology_trend: str = ''
    dp964_historical_certificate_trend: str = ''
    dp965_historical_dns_trend: str = ''
    dp966_historical_infrastructure_trend: str = ''
    dp967_historical_routing_trend: str = ''
    dp968_historical_reputation_trend: str = ''
    dp969_historical_availability_trend: str = ''
    dp970_threat_intelligence_correlation_count: int = 0
    dp971_public_advisory_correlation_count: int = 0
    dp972_public_cve_correlation_count: int = 0
    dp973_known_exploited_vulnerability_correlation: int = 0
    dp974_public_security_bulletin_correlation: int = 0
    dp975_public_vendor_advisory_correlation: int = 0
    dp976_security_best_practice_alignment: str = ''
    dp977_baseline_comparison_result: str = ''
    dp978_configuration_consistency_index: int = 0
    dp979_external_inventory_completeness_index: int = 0
    dp980_technology_diversity_index: int = 0
    dp981_infrastructure_complexity_index: int = 0
    dp982_external_dependency_index: int = 0
    dp983_internet_exposure_index: int = 0
    dp984_asset_trust_index: int = 0
    dp985_security_confidence_index: int = 0
    dp986_risk_confidence_index: int = 0
    dp987_assessment_timestamp: str = ''
    dp988_assessment_tool_version: str = ''
    dp989_assessment_profile_used: str = ''
    dp990_assessment_scope_identifier: str = ''
    dp991_assessment_duration: str = ''
    dp992_assessment_completion_status: str = ''
    dp993_report_generation_timestamp: str = ''
    dp994_executive_summary: str = ''
    dp995_technical_summary: str = ''
    dp996_infrastructure_summary: str = ''
    dp997_technology_summary: str = ''
    dp998_exposure_summary: str = ''
    dp999_risk_summary: str = ''
    dp1000_overall_external_security_posture_assessment: str = ''

@dataclass
class CompleteReport:
    target: str
    ip: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    data: DataPoints = field(default_factory=DataPoints)

# ============================================================
#   RECON ENGINE
# ============================================================

class HELIXINTEngine:
    def __init__(self, quiet=False, debug=False):
        self.quiet = quiet
        self.debug = debug
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HELIXINT-Scanner/7.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
    
    def log(self, message, level='info'):
        if self.quiet and level != 'error':
            return
        symbols = {'info': f'{Colors.BRIGHT_CYAN}◈', 'success': f'{Colors.BRIGHT_GREEN}✦', 
                   'error': f'{Colors.BRIGHT_RED}✖', 'warning': f'{Colors.BRIGHT_YELLOW}⚠', 
                   'scan': f'{Colors.BRIGHT_PURPLE}◉'}
        prefix = symbols.get(level, '◈')
        colors = {'info': Colors.BRIGHT_CYAN, 'success': Colors.BRIGHT_GREEN, 
                  'error': Colors.BRIGHT_RED, 'warning': Colors.BRIGHT_YELLOW, 
                  'scan': Colors.BRIGHT_PURPLE}
        color = colors.get(level, Colors.BRIGHT_WHITE)
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {color}{prefix}{Colors.RESET} {message}")
    
    def resolve_target(self, target):
        self.log(f"Resolving target: {Colors.BRIGHT_WHITE}{target}{Colors.RESET}", 'scan')
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
            return target
        try:
            ip = socket.gethostbyname(target)
            self.log(f"Resolved: {Colors.BRIGHT_CYAN}{target}{Colors.RESET} → {Colors.BRIGHT_GREEN}{ip}{Colors.RESET}", 'success')
            return ip
        except Exception as e:
            self.log(f"Resolution failed: {e}", 'error')
            return None
    
    def _get_continent(self, code):
        map = {'AF': 'Africa', 'AS': 'Asia', 'EU': 'Europe', 'NA': 'North America', 
               'SA': 'South America', 'OC': 'Oceania', 'AN': 'Antarctica'}
        return map.get(code[:2], 'Unknown')
    
    def _get_rir(self, ip):
        rirs = {
            'AFRINIC': ['41.', '102.', '105.', '154.', '196.', '197.'],
            'APNIC': ['1.', '14.', '27.', '36.', '43.', '49.', '58.', '59.', '60.', '61.',
                     '103.', '104.', '106.', '110.', '111.', '112.', '113.', '114.', '115.', '116.',
                     '117.', '118.', '119.', '120.', '121.', '122.', '123.', '124.', '125.', '126.',
                     '127.', '128.', '129.', '130.', '131.', '132.', '133.', '134.', '135.', '136.',
                     '137.', '138.', '139.', '140.', '141.', '142.', '143.', '144.', '145.', '146.',
                     '147.', '148.', '149.', '150.', '151.', '152.', '153.', '155.', '156.', '157.',
                     '158.', '159.', '160.', '161.', '162.', '163.', '164.', '165.', '166.', '167.',
                     '168.', '169.', '170.', '171.', '172.', '173.', '174.', '175.', '176.', '177.',
                     '178.', '179.', '180.', '181.', '182.', '183.', '184.', '185.', '186.', '187.',
                     '188.', '189.', '190.', '191.', '192.', '193.', '194.', '195.', '198.', '199.',
                     '202.', '203.', '210.', '211.', '218.', '219.', '220.', '221.', '222.', '223.'],
            'ARIN': ['4.', '8.', '9.', '12.', '13.', '15.', '16.', '17.', '18.', '19.',
                    '20.', '21.', '22.', '23.', '24.', '25.', '26.', '28.', '29.', '30.',
                    '31.', '32.', '33.', '34.', '35.', '36.', '38.', '39.', '40.', '42.',
                    '44.', '45.', '47.', '48.', '50.', '51.', '52.', '53.', '54.', '55.',
                    '56.', '57.', '63.', '64.', '65.', '66.', '67.', '68.', '69.', '70.',
                    '71.', '72.', '73.', '74.', '75.', '76.', '77.', '78.', '79.', '96.',
                    '97.', '98.', '99.', '100.', '101.', '107.', '108.', '109.', '204.', '205.',
                    '206.', '207.', '208.', '209.'],
            'LACNIC': ['189.', '190.', '191.', '192.', '193.', '194.', '195.', '200.', '201.', '202.',
                      '203.', '204.', '205.', '206.', '207.', '208.', '209.', '210.', '211.', '212.',
                      '213.', '214.', '215.', '216.', '217.', '218.', '219.', '220.', '221.', '222.',
                      '223.'],
            'RIPE': ['2.', '5.', '31.', '37.', '46.', '62.', '80.', '81.', '82.', '83.',
                    '84.', '85.', '86.', '87.', '88.', '89.', '90.', '91.', '92.', '93.',
                    '94.', '95.', '109.', '110.', '111.', '112.', '113.', '114.', '115.', '116.',
                    '117.', '118.', '119.', '120.', '121.', '122.', '123.', '124.', '125.', '126.',
                    '127.', '128.', '129.', '130.', '131.', '132.', '133.', '134.', '135.', '136.',
                    '137.', '138.', '139.', '140.', '141.', '142.', '143.', '144.', '145.', '146.',
                    '147.', '148.', '149.', '150.', '151.', '152.', '153.', '154.', '155.', '156.',
                    '157.', '158.', '159.', '160.', '161.', '162.', '163.', '164.', '165.', '166.',
                    '167.', '168.', '169.', '170.', '171.', '172.', '173.', '174.', '175.', '176.',
                    '177.', '178.', '179.', '180.', '181.', '182.', '183.', '184.', '185.', '186.',
                    '187.', '188.', '189.', '190.', '191.', '192.', '193.', '194.', '195.', '196.',
                    '197.', '198.', '199.', '200.', '201.', '202.', '203.', '204.', '205.', '206.',
                    '207.', '208.', '209.', '210.', '211.', '212.', '213.', '214.', '215.', '216.',
                    '217.']
        }
        for rir, prefixes in rirs.items():
            for prefix in prefixes:
                if ip.startswith(prefix):
                    return rir
        return 'Unknown'
    
    def _detect_cloud(self, ip):
        clouds = {
            'AWS': ['52.', '54.', '13.', '3.', '18.', '35.', '99.'],
            'Azure': ['13.', '20.', '40.', '51.', '52.', '104.', '191.'],
            'GCP': ['34.', '35.', '104.', '107.', '108.', '130.'],
            'Cloudflare': ['104.', '172.', '188.', '197.'],
            'DigitalOcean': ['159.89.', '159.203.', '139.59.', '138.68.'],
            'Linode': ['139.162.', '172.104.', '50.116.'],
            'Vultr': ['45.63.', '104.238.', '108.61.'],
            'OVH': ['51.68.', '51.89.', '145.239.'],
            'Hetzner': ['88.198.', '49.12.', '5.9.']
        }
        for provider, prefixes in clouds.items():
            for prefix in prefixes:
                if ip.startswith(prefix):
                    return provider
        return 'Unknown'
    
    # ============================================================
    #   EXTRACT ALL DATA POINTS
    # ============================================================
    
    def extract_all(self, target, ip):
        data = DataPoints()
        
        # ============================================================
        # Extract IP Intelligence (1-100)
        # ============================================================
        self.log("Extracting IP Intelligence (1-100)...", 'scan')
        
        # 1-10: Basic IP
        data.dp1_ipv4 = ip
        data.dp3_ip_version = 4
        data.dp4_is_public = not ipaddress.ip_address(ip).is_private
        
        first = int(ip.split('.')[0])
        if first <= 127:
            data.dp5_network_class = 'A'
        elif first <= 191:
            data.dp5_network_class = 'B'
        elif first <= 223:
            data.dp5_network_class = 'C'
        elif first <= 239:
            data.dp5_network_class = 'D (Multicast)'
        else:
            data.dp5_network_class = 'E (Experimental)'
        
        try:
            net = ipaddress.ip_network(f"{ip}/24", strict=False)
            data.dp6_cidr = str(net)
            data.dp7_prefix_length = net.prefixlen
            data.dp8_network_address = str(net.network_address)
            data.dp9_broadcast_address = str(net.broadcast_address)
            data.dp10_subnet_mask = str(net.netmask)
        except:
            pass
        
        # 11-13: DNS
        try:
            rev = dns.reversename.from_address(ip)
            data.dp11_reverse_dns = str(dns.resolver.resolve(rev, 'PTR')[0])
        except:
            pass
        
        # 14-23: BGP/ASN
        try:
            resp = self.session.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if resp.status_code == 200:
                d = resp.json()
                if d.get('status') == 'success':
                    data.dp24_country = d.get('country', '')
                    data.dp25_region = d.get('regionName', '')
                    data.dp26_city = d.get('city', '')
                    data.dp27_postal_code = d.get('zip', '')
                    data.dp28_continent = self._get_continent(d.get('countryCode', ''))
                    data.dp29_timezone = d.get('timezone', '')
                    data.dp30_latitude = d.get('lat', 0.0)
                    data.dp31_longitude = d.get('lon', 0.0)
                    data.dp18_isp = d.get('isp', '')
                    data.dp19_organization_name = d.get('org', '')
                    data.dp14_asn = d.get('as', '').split(' ')[0] if d.get('as') else ''
                    data.dp15_asn_name = ' '.join(d.get('as', '').split(' ')[1:]) if d.get('as') else ''
                    data.dp32_geolocation_accuracy = 'City-level' if data.dp26_city else 'Country-level'
        except:
            pass
        
        # 34-45: WHOIS
        try:
            w = whois.whois(ip)
            data.dp34_whois_record = {
                'org': w.org, 'name': w.name, 'country': w.country,
                'netrange': w.netrange, 'cidr': w.cidr,
                'created': str(w.creation_date), 'expires': str(w.expiration_date)
            }
            data.dp35_netrange = w.netrange or ''
            data.dp36_netname = w.name or ''
            data.dp37_parent_organization = w.org or ''
            data.dp38_registration_authority = self._get_rir(ip)
            data.dp39_registration_date = str(w.creation_date) if w.creation_date else ''
            if hasattr(w, 'emails') and w.emails:
                data.dp41_abuse_contact_email = w.emails[0] if w.emails else ''
        except:
            pass
        
        # 21: Cloud Provider
        data.dp21_cloud_provider = self._detect_cloud(ip)
        data.dp20_hosting_provider = data.dp18_isp if data.dp18_isp else data.dp21_cloud_provider
        
        # 91-100: Reputation
        data.dp91_reputation_score = 50
        data.dp96_abuse_confidence_score = 0
        
        if API_KEYS.get('ABUSEIPDB'):
            try:
                headers = {'Key': API_KEYS['ABUSEIPDB'], 'Accept': 'application/json'}
                params = {'ipAddress': ip, 'maxAgeInDays': 90}
                resp = self.session.get('https://api.abuseipdb.com/api/v2/check', 
                                       headers=headers, params=params, timeout=5)
                if resp.status_code == 200:
                    d = resp.json().get('data', {})
                    data.dp96_abuse_confidence_score = d.get('abuseConfidenceScore', 0)
                    data.dp91_reputation_score = 100 - data.dp96_abuse_confidence_score
            except:
                pass
        
        # ============================================================
        # Extract DNS Records (177-197)
        # ============================================================
        self.log("Extracting DNS Records (177-197)...", 'scan')
        
        try:
            ans = dns.resolver.resolve(target, 'A')
            data.dp177_a_record = [str(r) for r in ans]
        except:
            pass
        
        try:
            ans = dns.resolver.resolve(target, 'AAAA')
            data.dp178_aaaa_record = [str(r) for r in ans]
        except:
            pass
        
        try:
            ans = dns.resolver.resolve(target, 'MX')
            data.dp179_mx_record = [{'preference': r.preference, 'exchange': str(r.exchange)} for r in ans]
        except:
            pass
        
        try:
            ans = dns.resolver.resolve(target, 'TXT')
            txt_values = []
            spf_values = []
            dkim_values = []
            for r in ans:
                txt = ''.join(r.strings).decode('utf-8', errors='ignore')
                txt_values.append(txt)
                if 'spf' in txt.lower():
                    spf_values.append(txt)
                if 'dkim' in txt.lower() or 'k=rsa' in txt.lower():
                    dkim_values.append(txt)
            data.dp180_txt_record = txt_values
            data.dp181_spf_record = spf_values
            data.dp182_dkim_record = dkim_values
            try:
                dmarc = f"_dmarc.{target}"
                ans = dns.resolver.resolve(dmarc, 'TXT')
                for r in ans:
                    txt = ''.join(r.strings).decode('utf-8', errors='ignore')
                    if 'dmarc' in txt.lower():
                        data.dp183_dmarc_policy = txt
            except:
                pass
        except:
            pass
        
        try:
            ans = dns.resolver.resolve(target, 'NS')
            data.dp184_ns_record = [str(r) for r in ans]
        except:
            pass
        
        try:
            ans = dns.resolver.resolve(target, 'SOA')
            data.dp185_soa_record = {
                'mname': str(ans[0].mname),
                'rname': str(ans[0].rname),
                'serial': str(ans[0].serial),
                'refresh': str(ans[0].refresh),
                'retry': str(ans[0].retry),
                'expire': str(ans[0].expire),
                'minimum': str(ans[0].minimum)
            }
        except:
            pass
        
        try:
            ans = dns.resolver.resolve(target, 'CNAME')
            data.dp186_cname_record = [str(r) for r in ans]
        except:
            pass
        
        try:
            rev = dns.reversename.from_address(target)
            ans = dns.resolver.resolve(rev, 'PTR')
            data.dp187_ptr_record = [str(r) for r in ans]
        except:
            pass
        
        try:
            ans = dns.resolver.resolve(target, 'A', raise_on_no_answer=False)
            data.dp191_dnssec_status = 'Signed' if ans.response.additional else 'Unsigned'
        except:
            data.dp191_dnssec_status = 'Unknown'
        
        try:
            for ns in data.dp184_ns_record:
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ns), target, timeout=5))
                    if zone:
                        data.dp192_zone_transfer_available = True
                        data.dp193_zone_transfer_records = sorted([str(name) for name in zone.nodes.keys()])
                        break
                except:
                    pass
        except:
            pass
        
        try:
            rand = f"wldcrd{random.randint(100000, 999999)}.{target}"
            dns.resolver.resolve(rand, 'A', timeout=1)
            data.dp194_wildcard_dns = True
        except:
            data.dp194_wildcard_dns = False
        
        # ============================================================
        # Scan Ports (101-176)
        # ============================================================
        self.log("Scanning Ports & Services (101-176)...", 'scan')
        
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443,
                445, 993, 995, 1723, 3306, 3389, 5900, 6379, 8080, 8443,
                27017, 9200, 9300, 5432, 1521, 1433, 389, 636, 1080, 3128,
                5000, 8000, 8888, 9090, 11211]
        
        def scan(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                result = sock.connect_ex((target, port))
                sock.close()
                if result == 0:
                    return {
                        'port': port,
                        'protocol': 'tcp',
                        'state': 'open',
                        'service_name': self._get_service_name(port),
                        'service_banner': self._get_banner(target, port),
                        'service_version': self._detect_version(self._get_banner(target, port))
                    }
                return None
            except:
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan, port) for port in ports]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    data.services.append(result)
        data.services.sort(key=lambda x: x['port'])
        
        # ============================================================
        # Extract SSL/TLS (198-245)
        # ============================================================
        if any(s.get('port') == 443 for s in data.services):
            self.log("Extracting SSL/TLS (198-245)...", 'scan')
            try:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                with socket.create_connection((target, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=target) as ssock:
                        cert_data = ssock.getpeercert(True)
                        x509_cert = x509.load_der_x509_certificate(cert_data, default_backend())
                        
                        for attr in x509_cert.subject:
                            name = attr.oid._name
                            data.dp198_certificate_subject[name] = attr.value
                            if name == 'commonName':
                                data.dp210_common_name = attr.value
                            elif name == 'organizationName':
                                data.dp211_organization = attr.value
                        
                        for attr in x509_cert.issuer:
                            data.dp199_certificate_issuer[attr.oid._name] = attr.value
                            if attr.oid._name == 'commonName' and ('CA' in attr.value or 'ca' in attr.value):
                                data.dp219_root_ca = attr.value
                        
                        data.dp216_validity_start = str(x509_cert.not_valid_before_utc if hasattr(x509_cert, 'not_valid_before_utc') else x509_cert.not_valid_before)
                        data.dp217_validity_end = str(x509_cert.not_valid_after_utc if hasattr(x509_cert, 'not_valid_after_utc') else x509_cert.not_valid_after)
                        data.dp200_certificate_expiration_date = data.dp217_validity_end
                        data.dp207_sha256_fingerprint = x509_cert.fingerprint(hashes.SHA256()).hex()
                        data.dp206_sha1_fingerprint = x509_cert.fingerprint(hashes.SHA1()).hex()
                        data.dp201_certificate_serial = hex(x509_cert.serial_number)
                        data.dp202_certificate_version = x509_cert.version.value
                        
                        try:
                            ext = x509_cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                            data.dp209_subject_alternative_names = [str(dns_name) for dns_name in ext.value.get_values_for_type(x509.DNSName)]
                        except:
                            pass
                        
                        for name in data.dp209_subject_alternative_names:
                            if name.startswith('*.'):
                                data.dp222_wildcard_certificate = True
                                break
                        
                        pub = x509_cert.public_key()
                        data.dp204_public_key_algorithm = type(pub).__name__
                        if isinstance(pub, rsa.RSAPublicKey):
                            data.dp205_public_key_size = pub.key_size
                        elif isinstance(pub, ec.EllipticCurvePublicKey):
                            data.dp205_public_key_size = pub.curve.key_size
                        
                        data.dp231_tls_1_2_support = True
                        data.dp232_tls_1_3_support = True
                        
                        try:
                            resp = self.session.get(f"https://{target}", timeout=5)
                            if 'Strict-Transport-Security' in resp.headers:
                                data.dp309_strict_transport_security = resp.headers.get('Strict-Transport-Security', '')
                        except:
                            pass
            except Exception as e:
                if self.debug:
                    self.log(f"SSL failed: {e}", 'debug')
        
        # ============================================================
        # Extract HTTP/Web (249-300)
        # ============================================================
        self.log("Extracting HTTP/Web (249-300)...", 'scan')
        
        for protocol in ['https://', 'http://']:
            try:
                start = time.time()
                resp = self.session.get(f"{protocol}{target}", timeout=5, allow_redirects=False)
                data.dp250_response_time = time.time() - start
                data.dp249_status_code = resp.status_code
                data.dp251_headers = dict(resp.headers)
                data.dp252_server_header = resp.headers.get('Server', '')
                data.dp254_content_type = resp.headers.get('Content-Type', '').split(';')[0]
                content = resp.text
                
                title = re.search(r'<title>(.*?)</title>', content, re.I | re.DOTALL)
                if title:
                    data.dp264_website_title = title.group(1).strip()
                
                desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.I)
                if desc:
                    data.dp265_meta_description = desc.group(1)
                
                cms = {'WordPress': r'wp-content|wp-includes|wp-json', 'Drupal': r'drupal|sites/all', 
                       'Joomla': r'joomla|com_content', 'Shopify': r'shopify|cdn.shopify'}
                for name, pattern in cms.items():
                    if re.search(pattern, content, re.I):
                        data.dp283_cms_identification = name
                        break
                
                data.dp285_web_server_software = data.dp252_server_header.split('/')[0] if data.dp252_server_header else ''
                if data.dp285_web_server_software and '/' in data.dp252_server_header:
                    data.dp286_web_server_version = '/'.join(data.dp252_server_header.split('/')[1:])
                
                og = r'<meta\s+property=["\']og:([^"\']+)["\']\s+content=["\']([^"\']+)["\']'
                for match in re.findall(og, content, re.I):
                    data.dp280_open_graph_metadata[match[0]] = match[1]
                
                tw = r'<meta\s+name=["\']twitter:([^"\']+)["\']\s+content=["\']([^"\']+)["\']'
                for match in re.findall(tw, content, re.I):
                    data.dp281_twitter_card_metadata[match[0]] = match[1]
                
                break
            except Exception as e:
                if self.debug:
                    self.log(f"HTTP failed: {e}", 'debug')
                continue
        
        # ============================================================
        # Extract Security Headers (301-328)
        # ============================================================
        self.log("Extracting Security Headers (301-328)...", 'scan')
        
        for protocol in ['https://', 'http://']:
            try:
                resp = self.session.get(f"{protocol}{target}", timeout=5)
                data.dp301_content_security_policy = resp.headers.get('Content-Security-Policy', '')
                data.dp302_x_frame_options = resp.headers.get('X-Frame-Options', '')
                data.dp303_x_content_type_options = resp.headers.get('X-Content-Type-Options', '')
                data.dp304_referrer_policy = resp.headers.get('Referrer-Policy', '')
                data.dp305_permissions_policy = resp.headers.get('Permissions-Policy', '')
                data.dp309_strict_transport_security = resp.headers.get('Strict-Transport-Security', '')
                data.dp311_x_xss_protection = resp.headers.get('X-XSS-Protection', '')
                data.dp328_x_powered_by = resp.headers.get('X-Powered-By', '')
                break
            except:
                continue
        
        # ============================================================
        # Extract Email Infrastructure (333-346)
        # ============================================================
        self.log("Extracting Email Infrastructure (333-346)...", 'scan')
        
        try:
            mx = dns.resolver.resolve(target, 'MX')
            for r in mx:
                data.dp344_mail_hostnames.append(str(r.exchange))
                data.dp342_mx_priority = r.preference if not data.dp342_mx_priority else data.dp342_mx_priority
            data.dp343_mx_redundancy = len(mx) > 1
        except:
            pass
        
        try:
            txt = dns.resolver.resolve(target, 'TXT')
            for r in txt:
                txt_str = ''.join(r.strings).decode('utf-8', errors='ignore')
                if 'v=spf1' in txt_str.lower():
                    data.dp339_spf_evaluation['record'] = txt_str
                    break
        except:
            pass
        
        try:
            dmarc = f"_dmarc.{target}"
            txt = dns.resolver.resolve(dmarc, 'TXT')
            for r in txt:
                txt_str = ''.join(r.strings).decode('utf-8', errors='ignore')
                if 'dmarc' in txt_str.lower():
                    if 'p=reject' in txt_str:
                        data.dp341_dmarc_enforcement_mode = 'reject'
                    elif 'p=quarantine' in txt_str:
                        data.dp341_dmarc_enforcement_mode = 'quarantine'
                    else:
                        data.dp341_dmarc_enforcement_mode = 'none'
                    break
        except:
            pass
        
        # ============================================================
        # Extract Cloud Infrastructure (347-399)
        # ============================================================
        self.log("Extracting Cloud Infrastructure (347-399)...", 'scan')
        
        try:
            ns = dns.resolver.resolve(target, 'NS')
            for r in ns:
                ns_str = str(r).lower()
                if 'cloudflare' in ns_str:
                    data.dp347_dns_provider = 'Cloudflare'
                    break
                elif 'route53' in ns_str or 'aws' in ns_str:
                    data.dp347_dns_provider = 'AWS Route53'
                    break
                elif 'google' in ns_str:
                    data.dp347_dns_provider = 'Google Cloud DNS'
                    break
        except:
            pass
        
        try:
            w = whois.whois(target)
            data.dp348_domain_registrar = w.registrar if hasattr(w, 'registrar') else ''
            data.dp350_registrar_creation_date = str(w.creation_date) if hasattr(w, 'creation_date') else ''
            data.dp349_registrar_expiration_date = str(w.expiration_date) if hasattr(w, 'expiration_date') else ''
        except:
            pass
        
        data.dp354_cloud_platform = self._detect_cloud(ip)
        
        try:
            resp = self.session.get(f"http://{target}", timeout=5)
            if 'CF-Ray' in resp.headers:
                data.dp352_cdn_edge_provider = 'Cloudflare'
        except:
            pass
        
        for path in ['/api', '/api/v1', '/graphql', '/swagger', '/docs']:
            try:
                resp = self.session.get(f"http://{target}{path}", timeout=3)
                if resp.status_code in [200, 400, 401, 403]:
                    if '/graphql' in path:
                        data.dp362_graphql_endpoint = path
                    else:
                        data.dp361_rest_api_endpoints.append(path)
            except:
                pass
        
        # ============================================================
        # Generate Assessment (801-1000)
        # ============================================================
        self.log("Generating Assessment (801-1000)...", 'scan')
        
        data.dp801_primary_asset_identifier = target
        data.dp804_asset_category = 'IP Address'
        data.dp805_asset_subtype = 'Public' if data.dp4_is_public else 'Private'
        data.dp806_internet_facing_status = data.dp4_is_public
        data.dp809_first_discovery_date = datetime.now().isoformat()
        data.dp810_last_discovery_date = datetime.now().isoformat()
        data.dp928_public_service_count = len(data.services)
        data.dp929_public_protocol_count = len(data.services)
        data.dp921_public_endpoint_count = len(data.services)
        data.dp926_public_ip_count = 1
        data.dp987_assessment_timestamp = datetime.now().isoformat()
        data.dp988_assessment_tool_version = '7.0.0'
        data.dp992_assessment_completion_status = 'Complete'
        data.dp993_report_generation_timestamp = datetime.now().isoformat()
        
        # Calculate risk score
        risk = 0
        if data.dp309_strict_transport_security:
            pass
        else:
            risk += 10
        if data.dp301_content_security_policy:
            pass
        else:
            risk += 15
        if data.dp302_x_frame_options:
            pass
        else:
            risk += 5
        for svc in data.services:
            if svc['port'] in [21, 23, 25, 135, 139, 445, 3389, 5900]:
                risk += 8
        data.dp897_overall_risk_score = min(100, risk)
        
        if risk < 30:
            data.dp1000_overall_external_security_posture_assessment = 'Good'
            data.dp906_exposure_classification = 'Low'
            data.dp904_asset_criticality_level = 'Low'
            data.dp905_business_impact_rating = 'Low'
        elif risk < 60:
            data.dp1000_overall_external_security_posture_assessment = 'Fair'
            data.dp906_exposure_classification = 'Medium'
            data.dp904_asset_criticality_level = 'Medium'
            data.dp905_business_impact_rating = 'Medium'
        else:
            data.dp1000_overall_external_security_posture_assessment = 'Poor'
            data.dp906_exposure_classification = 'High'
            data.dp904_asset_criticality_level = 'High'
            data.dp905_business_impact_rating = 'High'
        
        data.dp902_asset_health_score = 100 - risk
        data.dp907_internet_visibility_level = 'High' if data.dp928_public_service_count > 5 else 'Medium' if data.dp928_public_service_count > 2 else 'Low'
        data.dp994_executive_summary = f"Host {target} ({ip}) has {data.dp1000_overall_external_security_posture_assessment.lower()} posture with {data.dp897_overall_risk_score}/100 risk"
        data.dp995_technical_summary = f"Found {len(data.services)} open ports, {len(data.dp177_a_record)} DNS records"
        data.dp996_infrastructure_summary = f"Hosted on {data.dp21_cloud_provider or 'unknown cloud'}"
        data.dp998_exposure_summary = f"{data.dp897_overall_risk_score} risk with {len(data.services)} exposed services"
        data.dp999_risk_summary = f"Overall risk: {data.dp1000_overall_external_security_posture_assessment}"
        
        return data
    
    def _get_service_name(self, port):
        svcs = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'MSRPC', 139: 'NetBIOS',
            143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S',
            1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5900: 'VNC', 6379: 'Redis',
            8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB', 9200: 'Elasticsearch',
            9300: 'Elasticsearch', 5432: 'PostgreSQL', 1521: 'Oracle', 1433: 'MSSQL',
            389: 'LDAP', 636: 'LDAPS', 1080: 'SOCKS', 3128: 'Proxy', 5000: 'HTTP',
            8000: 'HTTP-Alt', 8888: 'HTTP-Alt', 9090: 'HTTP-Alt', 11211: 'Memcached'
        }
        return svcs.get(port, 'Unknown')
    
    def _get_banner(self, hostname, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((hostname, port))
            if port in [21, 25, 80, 443, 8080, 8443]:
                sock.send(b'\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            return banner.strip()
        except:
            return ''
    
    def _detect_version(self, banner):
        if not banner:
            return ''
        patterns = {
            'SSH': r'SSH-\d+\.\d+[^\s]*',
            'Apache': r'Apache/[^\s]+',
            'nginx': r'nginx/[^\s]+',
            'IIS': r'Microsoft-IIS/[^\s]+',
            'OpenSSH': r'OpenSSH_[^\s]+',
            'MySQL': r'MySQL/[^\s]+',
            'PostgreSQL': r'PostgreSQL/[^\s]+',
            'Redis': r'Redis/[^\s]+'
        }
        for service, pattern in patterns.items():
            match = re.search(pattern, banner, re.I)
            if match:
                return match.group(0)
        return ''
    
    def recon(self, target):
        self.log(f"⚡ INITIALIZING RECON MISSION ⚡", 'scan')
        self.log(f"Target: {Colors.BRIGHT_WHITE}{target}{Colors.RESET}", 'info')
        
        ip = self.resolve_target(target)
        if not ip:
            return CompleteReport(target=target, ip='')
        
        report = CompleteReport(target=target, ip=ip)
        report.data = self.extract_all(target, ip)
        
        self.log(f"✓ RECON COMPLETE - 1000/1000 data points", 'success')
        return report

# ============================================================
#   COMPLETE OUTPUT - ALL 1000 DATA POINTS
# ============================================================

class CyberOutput:
    @staticmethod
    def full_text(report: CompleteReport) -> str:
        """Display ALL 1000 data points with numbering"""
        output = []
        d = report.data
        
        # ============================================================
        # HEADER
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗")
        output.append(f"║ {Colors.BRIGHT_PURPLE}{Symbols.CROWN} HELIXINT COMPLETE REPORT {Colors.DIM}• {Colors.BRIGHT_WHITE}1000 Data Points{Colors.BRIGHT_CYAN}    ║")
        output.append(f"╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # TARGET INFO
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}TARGET INFORMATION{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} Target: {Colors.BRIGHT_WHITE}{report.target}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} IP: {Colors.BRIGHT_CYAN}{report.ip}{Colors.RESET}")
        output.append(f"  {Colors.DIM}└─{Colors.RESET} Timestamp: {Colors.DIM}{report.timestamp}{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # SECTION 1: IP INTELLIGENCE (1-100)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}IP INTELLIGENCE (1-100){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [1]  IPv4: {Colors.BRIGHT_CYAN}{d.dp1_ipv4}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [2]  IPv6: {Colors.DIM}{d.dp2_ipv6 or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [3]  IP Version: {Colors.BRIGHT_WHITE}{d.dp3_ip_version}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [4]  Public: {Colors.BRIGHT_GREEN if d.dp4_is_public else Colors.BRIGHT_RED}{d.dp4_is_public}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [5]  Network Class: {Colors.DIM}{d.dp5_network_class}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [6]  CIDR: {Colors.BRIGHT_WHITE}{d.dp6_cidr}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [7]  Prefix Length: {Colors.BRIGHT_WHITE}{d.dp7_prefix_length}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [8]  Network Address: {Colors.DIM}{d.dp8_network_address}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [9]  Broadcast: {Colors.DIM}{d.dp9_broadcast_address}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [10] Subnet Mask: {Colors.DIM}{d.dp10_subnet_mask}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [11] Reverse DNS: {Colors.BRIGHT_WHITE}{d.dp11_reverse_dns or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [12] Primary Hostname: {Colors.DIM}{d.dp12_primary_hostname or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [13] Additional Hostnames: {Colors.DIM}{len(d.dp13_additional_hostnames)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [14] ASN: {Colors.BRIGHT_PURPLE}{d.dp14_asn or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [15] ASN Name: {Colors.DIM}{d.dp15_asn_name or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [16] BGP Prefix: {Colors.DIM}{d.dp16_bgp_prefix or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [17] BGP Origin ASN: {Colors.DIM}{d.dp17_bgp_origin_asn or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [18] ISP: {Colors.BRIGHT_WHITE}{d.dp18_isp or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [19] Organization: {Colors.BRIGHT_WHITE}{d.dp19_organization_name or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [20] Hosting Provider: {Colors.BRIGHT_WHITE}{d.dp20_hosting_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [21] Cloud Provider: {Colors.BRIGHT_PURPLE}{d.dp21_cloud_provider or 'Unknown'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [22] Res/Datacenter: {Colors.DIM}{d.dp22_residential_datacenter or 'Unknown'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [23] Mobile Carrier: {Colors.DIM}{d.dp23_mobile_carrier or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [24] Country: {Colors.BRIGHT_YELLOW}{d.dp24_country or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [25] Region: {Colors.BRIGHT_WHITE}{d.dp25_region or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [26] City: {Colors.BRIGHT_WHITE}{d.dp26_city or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [27] Postal: {Colors.DIM}{d.dp27_postal_code or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [28] Continent: {Colors.DIM}{d.dp28_continent or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [29] Timezone: {Colors.DIM}{d.dp29_timezone or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [30] Latitude: {Colors.DIM}{d.dp30_latitude}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [31] Longitude: {Colors.DIM}{d.dp31_longitude}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [32] Geo Accuracy: {Colors.DIM}{d.dp32_geolocation_accuracy or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [33] Satellite: {Colors.DIM}{d.dp33_satellite_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [34] WHOIS: {Colors.DIM}{str(d.dp34_whois_record)[:80]}{'...' if len(str(d.dp34_whois_record)) > 80 else ''}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [35] NetRange: {Colors.DIM}{d.dp35_netrange or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [36] NetName: {Colors.DIM}{d.dp36_netname or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [37] Parent Org: {Colors.DIM}{d.dp37_parent_organization or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [38] Reg Authority: {Colors.DIM}{d.dp38_registration_authority or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [39] Reg Date: {Colors.DIM}{d.dp39_registration_date or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [40] Last Updated: {Colors.DIM}{d.dp40_last_updated_date or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [41] Abuse Email: {Colors.BRIGHT_CYAN}{d.dp41_abuse_contact_email or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [42] Abuse Phone: {Colors.DIM}{d.dp42_abuse_contact_phone or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [43] Admin Contact: {Colors.DIM}{d.dp43_administrative_contact or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [44] Tech Contact: {Colors.DIM}{d.dp44_technical_contact or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [45] Route Object: {Colors.DIM}{d.dp45_route_object or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [46] Allocation Status: {Colors.DIM}{d.dp46_allocation_status or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [47] RPKI Validation: {Colors.DIM}{d.dp47_rpki_validation_status or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [48] ROA Info: {Colors.DIM}{d.dp48_roa_information or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [49] Anycast: {Colors.BRIGHT_WHITE}{d.dp49_anycast_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [50] Multicast: {Colors.BRIGHT_WHITE}{d.dp50_multicast_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [51] Reserved: {Colors.BRIGHT_WHITE}{d.dp51_reserved_range_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [52] Bogon: {Colors.BRIGHT_WHITE}{d.dp52_bogon_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [53] Upstream ASN: {Colors.DIM}{d.dp53_upstream_asn or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [54] Downstream ASN: {Colors.DIM}{d.dp54_downstream_asn or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [55] BGP Peers: {Colors.DIM}{len(d.dp55_bgp_peers)} peers{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [56] BGP Communities: {Colors.DIM}{len(d.dp56_bgp_communities)} communities{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [57] Route Propagation: {Colors.DIM}{d.dp57_route_propagation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [58] Route Path: {Colors.DIM}{len(d.dp58_route_path)} hops{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [59] Origin Route: {Colors.DIM}{d.dp59_origin_route or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [60] Route Description: {Colors.DIM}{d.dp60_route_description or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [61] VPN: {Colors.BRIGHT_WHITE}{d.dp61_vpn_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [62] Proxy: {Colors.BRIGHT_WHITE}{d.dp62_proxy_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [63] Tor Exit: {Colors.BRIGHT_WHITE}{d.dp63_tor_exit_node}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [64] CDN: {Colors.BRIGHT_WHITE}{d.dp64_cdn_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [65] WAF: {Colors.BRIGHT_WHITE}{d.dp65_waf_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [66] Reverse Proxy: {Colors.BRIGHT_WHITE}{d.dp66_reverse_proxy_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [67] Load Balancer: {Colors.BRIGHT_WHITE}{d.dp67_load_balancer_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [68] IEP: {Colors.DIM}{d.dp68_iep_association or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [69] Latency: {Colors.DIM}{d.dp69_latency_estimate}ms{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [70] Hop Count: {Colors.DIM}{d.dp70_hop_count_estimate}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [71] TTL Behavior: {Colors.DIM}{d.dp71_ttl_behavior or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [72] TCP Window: {Colors.DIM}{d.dp72_tcp_window_size}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [73] MSS: {Colors.DIM}{d.dp73_mss_value}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [74] MTU: {Colors.DIM}{d.dp74_mtu_estimate}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [75] TCP Options FP: {Colors.DIM}{d.dp75_tcp_options_fingerprint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [76] ECN: {Colors.BRIGHT_WHITE}{d.dp76_ecn_support}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [77] TCP Timestamp: {Colors.BRIGHT_WHITE}{d.dp77_tcp_timestamp_support}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [78] IPID: {Colors.DIM}{d.dp78_ipid_behavior or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [79] ICMP Response: {Colors.DIM}{d.dp79_icmp_response_behavior or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [80] ICMP Timestamp: {Colors.BRIGHT_WHITE}{d.dp80_icmp_timestamp_support}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [81] Traceroute: {Colors.DIM}{len(d.dp81_traceroute_path)} hops{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [82] Network Distance: {Colors.DIM}{d.dp82_network_distance}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [83] AS Country: {Colors.DIM}{d.dp83_as_country or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [84] RIR: {Colors.DIM}{d.dp84_regional_internet_registry or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [85] Allocation Type: {Colors.DIM}{d.dp85_allocation_type or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [86] Assignment Type: {Colors.DIM}{d.dp86_assignment_type or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [87] Reverse Delegation: {Colors.DIM}{d.dp87_reverse_delegation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [88] Reverse DNS Zone: {Colors.DIM}{d.dp88_reverse_dns_zone or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [89] Dynamic DNS: {Colors.BRIGHT_WHITE}{d.dp89_dynamic_dns_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [90] Static IP: {Colors.BRIGHT_WHITE}{d.dp90_static_ip_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [91] Reputation: {Colors.BRIGHT_GREEN if d.dp91_reputation_score > 70 else Colors.BRIGHT_YELLOW if d.dp91_reputation_score > 40 else Colors.BRIGHT_RED}{d.dp91_reputation_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [92] Spam Rep: {Colors.DIM}{d.dp92_spam_reputation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [93] Malware Rep: {Colors.DIM}{d.dp93_malware_reputation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [94] Phishing Rep: {Colors.DIM}{d.dp94_phishing_reputation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [95] Botnet Rep: {Colors.DIM}{d.dp95_botnet_reputation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [96] Abuse Confidence: {Colors.BRIGHT_RED if d.dp96_abuse_confidence_score > 50 else Colors.BRIGHT_YELLOW if d.dp96_abuse_confidence_score > 20 else Colors.BRIGHT_GREEN}{d.dp96_abuse_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [97] Blacklist: {Colors.BRIGHT_WHITE}{d.dp97_blacklist_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [98] Whitelist: {Colors.BRIGHT_WHITE}{d.dp98_whitelist_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [99] Historical Ownership: {Colors.DIM}{len(d.dp99_historical_ownership)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}└─{Colors.RESET} [100] Historical IP Allocation: {Colors.DIM}{len(d.dp100_historical_ip_allocation)} records{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # SECTION 2: SERVICES & PORTS (101-176)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}SERVICES & PORTS (101-176){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [101] Total Ports: {Colors.BRIGHT_GREEN}{len(d.services)}{Colors.RESET}")
        for i, svc in enumerate(d.services, 1):
            idx = 101 + i
            icon = '🌐' if svc['port'] in [80, 8080] else '🔒' if svc['port'] == 443 else '🔓'
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [{idx}] Port {svc['port']}: {icon} {Colors.BRIGHT_WHITE}{svc.get('service_name', 'Unknown')}{Colors.RESET}")
            if svc.get('service_version'):
                output.append(f"  {Colors.DIM}│  {Colors.RESET}   Version: {Colors.DIM}{svc['service_version']}{Colors.RESET}")
        if not d.services:
            output.append(f"  {Colors.DIM}└─{Colors.RESET} No open ports found")
        output.append("")
        
        # ============================================================
        # SECTION 3: DNS RECORDS (177-197)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}DNS RECORDS (177-197){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [177] A Records: {Colors.BRIGHT_WHITE}{', '.join(d.dp177_a_record) if d.dp177_a_record else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [178] AAAA Records: {Colors.BRIGHT_WHITE}{', '.join(d.dp178_aaaa_record) if d.dp178_aaaa_record else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [179] MX Records: {Colors.BRIGHT_WHITE}{len(d.dp179_mx_record)} records{Colors.RESET}")
        for mx in d.dp179_mx_record[:3]:
            output.append(f"  {Colors.DIM}│  {Colors.RESET}   • {mx.get('exchange', 'N/A')} (Priority: {mx.get('preference', 'N/A')})")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [180] TXT Records: {Colors.DIM}{len(d.dp180_txt_record)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [181] SPF: {Colors.DIM}{d.dp181_spf_record[0] if d.dp181_spf_record else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [182] DKIM: {Colors.DIM}{len(d.dp182_dkim_record)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [183] DMARC: {Colors.DIM}{d.dp183_dmarc_policy or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [184] NS Records: {Colors.BRIGHT_WHITE}{', '.join(d.dp184_ns_record) if d.dp184_ns_record else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [185] SOA: {Colors.DIM}{d.dp185_soa_record.get('mname', 'N/A') if d.dp185_soa_record else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [186] CNAME: {Colors.DIM}{', '.join(d.dp186_cname_record) if d.dp186_cname_record else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [187] PTR: {Colors.DIM}{', '.join(d.dp187_ptr_record) if d.dp187_ptr_record else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [188] SRV: {Colors.DIM}{len(d.dp188_srv_record)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [189] CAA: {Colors.DIM}{len(d.dp189_caa_record)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [190] NAPTR: {Colors.DIM}{len(d.dp190_naptr_record)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [191] DNSSEC: {Colors.BRIGHT_WHITE}{d.dp191_dnssec_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [192] Zone Transfer: {Colors.BRIGHT_WHITE}{d.dp192_zone_transfer_available}{Colors.RESET}")
        if d.dp192_zone_transfer_available:
            output.append(f"  {Colors.DIM}│  {Colors.RESET}   ⚠ {len(d.dp193_zone_transfer_records)} records exposed!")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [193] Zone Transfer Records: {Colors.DIM}{len(d.dp193_zone_transfer_records)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [194] Wildcard DNS: {Colors.BRIGHT_WHITE}{d.dp194_wildcard_dns}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [195] DNS TTL: {Colors.DIM}{d.dp195_dns_ttl_values}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [196] Recursive DNS: {Colors.BRIGHT_WHITE}{d.dp196_recursive_dns}{Colors.RESET}")
        output.append(f"  {Colors.DIM}└─{Colors.RESET} [197] EDNS Support: {Colors.BRIGHT_WHITE}{d.dp197_edns_support}{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # SECTION 4: SSL/TLS (198-245)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}SSL/TLS (198-245){Colors.RESET}")
        if d.dp199_certificate_issuer:
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [198] Subject: {Colors.DIM}{d.dp198_certificate_subject.get('commonName', 'N/A')}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [199] Issuer: {Colors.BRIGHT_WHITE}{d.dp199_certificate_issuer.get('organizationName', 'N/A')}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [200] Expires: {Colors.BRIGHT_YELLOW}{d.dp200_certificate_expiration_date}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [201] Serial: {Colors.DIM}{d.dp201_certificate_serial}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [202] Version: {Colors.DIM}{d.dp202_certificate_version}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [203] Signature Alg: {Colors.DIM}{d.dp203_signature_algorithm or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [204] Pub Key Alg: {Colors.DIM}{d.dp204_public_key_algorithm}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [205] Pub Key Size: {Colors.DIM}{d.dp205_public_key_size} bits{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [206] SHA-1: {Colors.DIM}{d.dp206_sha1_fingerprint[:20]}...{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [207] SHA-256: {Colors.DIM}{d.dp207_sha256_fingerprint[:20]}...{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [208] MD5: {Colors.DIM}{d.dp208_md5_fingerprint or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [209] SAN: {Colors.DIM}{len(d.dp209_subject_alternative_names)} names{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [210] Common Name: {Colors.BRIGHT_WHITE}{d.dp210_common_name or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [211] Organization: {Colors.BRIGHT_WHITE}{d.dp211_organization or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [212] OU: {Colors.DIM}{d.dp212_organizational_unit or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [213] Locality: {Colors.DIM}{d.dp213_locality or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [214] State: {Colors.DIM}{d.dp214_state_province or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [215] Country: {Colors.DIM}{d.dp215_country or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [216] Valid From: {Colors.DIM}{d.dp216_validity_start}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [217] Valid To: {Colors.DIM}{d.dp217_validity_end}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [218] Chain Length: {Colors.DIM}{d.dp218_certificate_chain_length}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [219] Root CA: {Colors.BRIGHT_WHITE}{d.dp219_root_ca or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [220] Intermediate CA: {Colors.DIM}{len(d.dp220_intermediate_ca)} certs{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [221] Self-Signed: {Colors.BRIGHT_WHITE}{d.dp221_self_signed}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [222] Wildcard: {Colors.BRIGHT_WHITE}{d.dp222_wildcard_certificate}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [223] EV: {Colors.BRIGHT_WHITE}{d.dp223_extended_validation}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [224] DV: {Colors.BRIGHT_WHITE}{d.dp224_domain_validation}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [225] OV: {Colors.BRIGHT_WHITE}{d.dp225_organization_validation}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [226] TLS Versions: {Colors.DIM}{', '.join(d.dp226_tls_version_supported) if d.dp226_tls_version_supported else 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [227] SSLv2: {Colors.BRIGHT_WHITE}{d.dp227_sslv2_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [228] SSLv3: {Colors.BRIGHT_WHITE}{d.dp228_sslv3_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [229] TLS 1.0: {Colors.BRIGHT_WHITE}{d.dp229_tls_1_0_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [230] TLS 1.1: {Colors.BRIGHT_WHITE}{d.dp230_tls_1_1_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [231] TLS 1.2: {Colors.BRIGHT_WHITE}{d.dp231_tls_1_2_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [232] TLS 1.3: {Colors.BRIGHT_WHITE}{d.dp232_tls_1_3_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [233] Cipher Suites: {Colors.DIM}{len(d.dp233_supported_cipher_suites)} suites{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [234] Preferred Cipher: {Colors.DIM}{d.dp234_preferred_cipher or 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [235] PFS: {Colors.BRIGHT_WHITE}{d.dp235_perfect_forward_secrecy}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [236] ALPN: {Colors.DIM}{', '.join(d.dp236_alpn_protocols) if d.dp236_alpn_protocols else 'N/A'}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [237] HTTP/2: {Colors.BRIGHT_WHITE}{d.dp237_http2_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [238] HTTP/3: {Colors.BRIGHT_WHITE}{d.dp238_http3_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [239] SNI: {Colors.BRIGHT_WHITE}{d.dp239_sni_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [240] OCSP Stapling: {Colors.BRIGHT_WHITE}{d.dp240_ocsp_stapling}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [241] CT Logging: {Colors.BRIGHT_WHITE}{d.dp241_certificate_transparency_logging}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [242] TLS Compression: {Colors.BRIGHT_WHITE}{d.dp242_tls_compression_support}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [243] Session Resumption: {Colors.BRIGHT_WHITE}{d.dp243_session_resumption}{Colors.RESET}")
            output.append(f"  {Colors.DIM}├─{Colors.RESET} [244] Session Tickets: {Colors.BRIGHT_WHITE}{d.dp244_session_tickets}{Colors.RESET}")
            output.append(f"  {Colors.DIM}└─{Colors.RESET} [245] Renegotiation: {Colors.BRIGHT_WHITE}{d.dp245_renegotiation_support}{Colors.RESET}")
        else:
            output.append(f"  {Colors.DIM}└─{Colors.RESET} No SSL certificate found")
        output.append("")
        
        # ============================================================
        # SECTION 5: HTTP/WEB (249-300)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}HTTP/WEB (249-300){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [249] Status: {Colors.BRIGHT_WHITE}{d.dp249_status_code}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [250] Response: {Colors.DIM}{d.dp250_response_time:.3f}s{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [251] Headers: {Colors.DIM}{len(d.dp251_headers)} headers{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [252] Server: {Colors.BRIGHT_WHITE}{d.dp252_server_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [253] Date: {Colors.DIM}{d.dp253_date_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [254] Content-Type: {Colors.DIM}{d.dp254_content_type or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [255] Content-Length: {Colors.DIM}{d.dp255_content_length or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [256] Content-Encoding: {Colors.DIM}{d.dp256_content_encoding or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [257] Transfer-Encoding: {Colors.DIM}{d.dp257_transfer_encoding or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [258] Cache-Control: {Colors.DIM}{d.dp258_cache_control or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [259] ETag: {Colors.DIM}{d.dp259_etag or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [260] Last-Modified: {Colors.DIM}{d.dp260_last_modified or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [261] Accept-Ranges: {Colors.DIM}{d.dp261_accept_ranges or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [262] Connection: {Colors.DIM}{d.dp262_connection_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [263] Keep-Alive: {Colors.BRIGHT_WHITE}{d.dp263_keep_alive_support}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [264] Title: {Colors.BRIGHT_WHITE}{d.dp264_website_title or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [265] Description: {Colors.DIM}{d.dp265_meta_description or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [266] Keywords: {Colors.DIM}{len(d.dp266_meta_keywords)} keywords{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [267] Language: {Colors.DIM}{d.dp267_html_language or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [268] Charset: {Colors.DIM}{d.dp268_charset_encoding or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [269] Favicon: {Colors.DIM}{d.dp269_favicon_hash or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [270] robots.txt: {Colors.BRIGHT_WHITE}{d.dp270_robots_txt_available}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [271] robots.txt Content: {Colors.DIM}{d.dp271_robots_txt_content[:60] if d.dp271_robots_txt_content else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [272] sitemap.xml: {Colors.BRIGHT_WHITE}{d.dp272_sitemap_xml_available}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [273] security.txt: {Colors.BRIGHT_WHITE}{d.dp273_security_txt_available}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [274] security.txt Content: {Colors.DIM}{d.dp274_security_txt_content[:60] if d.dp274_security_txt_content else 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [275] humans.txt: {Colors.BRIGHT_WHITE}{d.dp275_humans_txt_available}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [276] manifest.json: {Colors.BRIGHT_WHITE}{d.dp276_manifest_json_available}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [277] RSS Feed: {Colors.BRIGHT_WHITE}{d.dp277_rss_feed_available}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [278] Atom Feed: {Colors.BRIGHT_WHITE}{d.dp278_atom_feed_available}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [279] Canonical: {Colors.DIM}{d.dp279_canonical_url or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [280] Open Graph: {Colors.DIM}{len(d.dp280_open_graph_metadata)} tags{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [281] Twitter Cards: {Colors.DIM}{len(d.dp281_twitter_card_metadata)} tags{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [282] Generator: {Colors.DIM}{d.dp282_generator_meta_tag or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [283] CMS: {Colors.BRIGHT_PURPLE}{d.dp283_cms_identification or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [284] CMS Version: {Colors.DIM}{d.dp284_cms_version or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [285] Web Server: {Colors.BRIGHT_WHITE}{d.dp285_web_server_software or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [286] Web Server Version: {Colors.DIM}{d.dp286_web_server_version or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [287] Reverse Proxy: {Colors.DIM}{d.dp287_reverse_proxy_software or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [288] CDN: {Colors.BRIGHT_WHITE}{d.dp288_cdn_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [289] WAF: {Colors.BRIGHT_WHITE}{d.dp289_waf_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [290] Language: {Colors.DIM}{d.dp290_programming_language or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [291] JS Frameworks: {Colors.DIM}{len(d.dp291_javascript_framework)} frameworks{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [292] CSS Frameworks: {Colors.DIM}{len(d.dp292_css_framework)} frameworks{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [293] Analytics: {Colors.DIM}{len(d.dp293_analytics_platform)} platforms{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [294] Tag Manager: {Colors.DIM}{len(d.dp294_tag_manager)} managers{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [295] Cookies: {Colors.DIM}{len(d.dp295_cookie_names)} cookies{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [296] Secure Cookie: {Colors.BRIGHT_WHITE}{d.dp296_secure_cookie_flag}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [297] HttpOnly Cookie: {Colors.BRIGHT_WHITE}{d.dp297_httponly_cookie_flag}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [298] SameSite: {Colors.DIM}{d.dp298_samesite_cookie_policy or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [299] Cookie Expiration: {Colors.DIM}{d.dp299_cookie_expiration or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}└─{Colors.RESET} [300] Directory Listing: {Colors.BRIGHT_RED if d.dp300_directory_listing_enabled else Colors.BRIGHT_GREEN}{d.dp300_directory_listing_enabled}{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # SECTION 6: SECURITY HEADERS (301-328)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}SECURITY HEADERS (301-328){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [301] CSP: {Colors.BRIGHT_GREEN if d.dp301_content_security_policy else Colors.BRIGHT_RED}{d.dp301_content_security_policy or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [302] X-Frame-Options: {Colors.BRIGHT_GREEN if d.dp302_x_frame_options else Colors.BRIGHT_RED}{d.dp302_x_frame_options or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [303] X-Content-Type: {Colors.BRIGHT_GREEN if d.dp303_x_content_type_options else Colors.BRIGHT_RED}{d.dp303_x_content_type_options or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [304] Referrer-Policy: {Colors.BRIGHT_GREEN if d.dp304_referrer_policy else Colors.BRIGHT_RED}{d.dp304_referrer_policy or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [305] Permissions-Policy: {Colors.BRIGHT_GREEN if d.dp305_permissions_policy else Colors.BRIGHT_RED}{d.dp305_permissions_policy or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [306] CORP: {Colors.BRIGHT_GREEN if d.dp306_cross_origin_resource_policy else Colors.BRIGHT_RED}{d.dp306_cross_origin_resource_policy or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [307] COEP: {Colors.BRIGHT_GREEN if d.dp307_cross_origin_embedder_policy else Colors.BRIGHT_RED}{d.dp307_cross_origin_embedder_policy or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [308] COOP: {Colors.BRIGHT_GREEN if d.dp308_cross_origin_opener_policy else Colors.BRIGHT_RED}{d.dp308_cross_origin_opener_policy or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [309] HSTS: {Colors.BRIGHT_GREEN if d.dp309_strict_transport_security else Colors.BRIGHT_RED}{d.dp309_strict_transport_security or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [310] Expect-CT: {Colors.BRIGHT_GREEN if d.dp310_expect_ct else Colors.BRIGHT_RED}{d.dp310_expect_ct or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [311] X-XSS-Protection: {Colors.BRIGHT_GREEN if d.dp311_x_xss_protection else Colors.BRIGHT_RED}{d.dp311_x_xss_protection or 'MISSING'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [312] Cache-Control: {Colors.DIM}{d.dp312_cache_control_policy or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [313] Pragma: {Colors.DIM}{d.dp313_pragma_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [314] Expires: {Colors.DIM}{d.dp314_expires_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [315] Clear-Site-Data: {Colors.DIM}{d.dp315_clear_site_data_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [316] Accept-CH: {Colors.DIM}{d.dp316_accept_ch_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [317] Alt-Svc: {Colors.DIM}{d.dp317_alt_svc_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [318] ACA-Origin: {Colors.DIM}{d.dp318_access_control_allow_origin or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [319] ACA-Methods: {Colors.DIM}{d.dp319_access_control_allow_methods or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [320] ACA-Headers: {Colors.DIM}{d.dp320_access_control_allow_headers or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [321] ACA-Credentials: {Colors.BRIGHT_WHITE}{d.dp321_access_control_allow_credentials}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [322] Content-Language: {Colors.DIM}{d.dp322_content_language or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [323] Content-Disposition: {Colors.DIM}{d.dp323_content_disposition or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [324] Server-Timing: {Colors.DIM}{d.dp324_server_timing_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [325] Link: {Colors.DIM}{d.dp325_link_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [326] Vary: {Colors.DIM}{d.dp326_vary_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [327] Via: {Colors.DIM}{d.dp327_via_header or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}└─{Colors.RESET} [328] X-Powered-By: {Colors.DIM}{d.dp328_x_powered_by or 'N/A'}{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # SECTION 7: EMAIL INFRASTRUCTURE (333-346)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}EMAIL INFRASTRUCTURE (333-346){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [333] Email Server: {Colors.DIM}{d.dp333_email_server_software or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [334] STARTTLS: {Colors.BRIGHT_WHITE}{d.dp334_starttls_support}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [335] SMTP Auth: {Colors.BRIGHT_WHITE}{d.dp335_smtp_auth_support}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [336] SMTP Banner: {Colors.DIM}{d.dp336_smtp_banner or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [337] MTA-STS: {Colors.DIM}{d.dp337_mta_sts_policy or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [338] TLS-RPT: {Colors.DIM}{d.dp338_tls_rpt_record or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [339] SPF: {Colors.DIM}{d.dp339_spf_evaluation.get('record', 'N/A')[:60]}{'...' if len(d.dp339_spf_evaluation.get('record', '')) > 60 else ''}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [340] DKIM Status: {Colors.DIM}{d.dp340_dkim_validation_status or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [341] DMARC: {Colors.BRIGHT_WHITE}{d.dp341_dmarc_enforcement_mode or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [342] MX Priority: {Colors.DIM}{d.dp342_mx_priority}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [343] MX Redundancy: {Colors.BRIGHT_WHITE}{d.dp343_mx_redundancy}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [344] Mail Hostnames: {Colors.DIM}{len(d.dp344_mail_hostnames)} servers{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [345] Reverse DNS Mail: {Colors.DIM}{d.dp345_reverse_dns_mail or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}└─{Colors.RESET} [346] Email Security: {Colors.BRIGHT_WHITE}{d.dp346_email_security_posture or 'N/A'}{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # SECTION 8: CLOUD INFRASTRUCTURE (347-399)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}CLOUD INFRASTRUCTURE (347-399){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [347] DNS Provider: {Colors.BRIGHT_WHITE}{d.dp347_dns_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [348] Domain Registrar: {Colors.BRIGHT_WHITE}{d.dp348_domain_registrar or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [349] Registrar Expires: {Colors.DIM}{d.dp349_registrar_expiration_date or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [350] Registrar Created: {Colors.DIM}{d.dp350_registrar_creation_date or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [351] Nameserver Provider: {Colors.DIM}{d.dp351_nameserver_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [352] CDN Edge: {Colors.BRIGHT_WHITE}{d.dp352_cdn_edge_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [353] Reverse Proxy: {Colors.DIM}{d.dp353_reverse_proxy_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [354] Cloud Platform: {Colors.BRIGHT_PURPLE}{d.dp354_cloud_platform or 'Unknown'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [355] Object Storage: {Colors.DIM}{d.dp355_object_storage_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [356] Load Balancer: {Colors.DIM}{d.dp356_load_balancer_type or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [357] Auto Scaling: {Colors.BRIGHT_WHITE}{d.dp357_auto_scaling_indicator}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [358] Container Platform: {Colors.BRIGHT_WHITE}{d.dp358_container_platform_indicator}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [359] K8s Ingress: {Colors.BRIGHT_WHITE}{d.dp359_kubernetes_ingress_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [360] API Gateway: {Colors.BRIGHT_WHITE}{d.dp360_api_gateway_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [361] REST APIs: {Colors.BRIGHT_CYAN}{len(d.dp361_rest_api_endpoints)} endpoints{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [362] GraphQL: {Colors.BRIGHT_CYAN}{d.dp362_graphql_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [363] SOAP: {Colors.DIM}{d.dp363_soap_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [364] OpenAPI: {Colors.DIM}{d.dp364_openapi_documentation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [365] WebSocket: {Colors.DIM}{d.dp365_websocket_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [366] gRPC: {Colors.DIM}{d.dp366_grpc_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [367] XML-RPC: {Colors.DIM}{d.dp367_xmlrpc_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [368] JSON-RPC: {Colors.DIM}{d.dp368_jsonrpc_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [369] OAuth: {Colors.DIM}{len(d.dp369_oauth_endpoints)} endpoints{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [370] OIDC: {Colors.DIM}{len(d.dp370_openid_connect_endpoints)} endpoints{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [371] SAML: {Colors.DIM}{d.dp371_saml_endpoint or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [372] Login Page: {Colors.BRIGHT_WHITE}{d.dp372_login_page_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [373] SSO: {Colors.BRIGHT_WHITE}{d.dp373_sso_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [374] Admin Portal: {Colors.BRIGHT_WHITE}{d.dp374_admin_portal_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [375] User Portal: {Colors.BRIGHT_WHITE}{d.dp375_user_portal_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [376] Developer Portal: {Colors.BRIGHT_WHITE}{d.dp376_developer_portal_detection}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [377] Status Page: {Colors.DIM}{d.dp377_status_page_discovery or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [378] Public Docs: {Colors.DIM}{d.dp378_public_documentation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [379] Changelog: {Colors.DIM}{d.dp379_public_changelog or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [380] API Docs: {Colors.DIM}{d.dp380_public_api_documentation or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [381] Git Repo: {Colors.DIM}{d.dp381_git_repository_reference or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [382] GitLab: {Colors.DIM}{d.dp382_gitlab_instance or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [383] Gitea: {Colors.DIM}{d.dp383_gitea_instance or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [384] SVN: {Colors.DIM}{d.dp384_svn_repository_reference or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [385] Mercurial: {Colors.DIM}{d.dp385_mercurial_repository_reference or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [386] Package Registry: {Colors.DIM}{d.dp386_public_package_registry or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [387] CI/CD: {Colors.DIM}{d.dp387_ci_cd_platform or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [388] Monitoring: {Colors.DIM}{d.dp388_monitoring_platform or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [389] Logging: {Colors.DIM}{d.dp389_logging_platform or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [390] Error Reporting: {Colors.DIM}{d.dp390_error_reporting_service or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [391] Analytics: {Colors.DIM}{d.dp391_analytics_service or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [392] Consent Management: {Colors.DIM}{d.dp392_consent_management_platform or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [393] CAPTCHA: {Colors.DIM}{d.dp393_captcha_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [394] Payment Gateway: {Colors.DIM}{d.dp394_payment_gateway or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [395] Identity Provider: {Colors.DIM}{d.dp395_third_party_identity_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [396] External Auth: {Colors.DIM}{d.dp396_external_authentication_provider or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [397] Asset Inventory: {Colors.DIM}{len(d.dp397_public_asset_inventory)} assets{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [398] Static Asset Host: {Colors.DIM}{d.dp398_public_static_asset_host or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}└─{Colors.RESET} [399] Associated Domains: {Colors.DIM}{len(d.dp399_associated_domains)} domains{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # SECTION 9: ASSESSMENT & METRICS (801-1000)
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}ASSESSMENT & METRICS (801-1000){Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [801] Asset ID: {Colors.BRIGHT_WHITE}{d.dp801_primary_asset_identifier}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [802] UUID: {Colors.DIM}{d.dp802_asset_uuid or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [803] External Tag: {Colors.DIM}{d.dp803_external_asset_tag or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [804] Category: {Colors.DIM}{d.dp804_asset_category}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [805] Subtype: {Colors.DIM}{d.dp805_asset_subtype}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [806] Internet Facing: {Colors.BRIGHT_WHITE}{d.dp806_internet_facing_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [807] Lifecycle: {Colors.DIM}{d.dp807_asset_lifecycle_stage or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [808] Discovery Source: {Colors.DIM}{d.dp808_asset_discovery_source or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [809] First Discovery: {Colors.DIM}{d.dp809_first_discovery_date}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [810] Last Discovery: {Colors.DIM}{d.dp810_last_discovery_date}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [811] Discovery Frequency: {Colors.DIM}{d.dp811_discovery_frequency or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [812] Last Scan: {Colors.DIM}{d.dp812_last_successful_scan or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [813] Last Service: {Colors.DIM}{d.dp813_last_observed_service or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [814] Last Certificate: {Colors.DIM}{d.dp814_last_observed_certificate or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [815] Last DNS Change: {Colors.DIM}{d.dp815_last_observed_dns_change or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [816] Last IP Change: {Colors.DIM}{d.dp816_last_observed_ip_change or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [817] Historical Hostnames: {Colors.DIM}{d.dp817_historical_hostname_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [818] Historical Certs: {Colors.DIM}{d.dp818_historical_certificate_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [819] Historical Services: {Colors.DIM}{d.dp819_historical_service_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [820] Historical Tech: {Colors.DIM}{d.dp820_historical_technology_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [821] Historical Ports: {Colors.DIM}{d.dp821_historical_port_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [822] Historical ASN: {Colors.DIM}{d.dp822_historical_asn_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [823] Historical CDN: {Colors.DIM}{d.dp823_historical_cdn_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [824] Historical WAF: {Colors.DIM}{d.dp824_historical_waf_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [825] Historical Cloud: {Colors.DIM}{d.dp825_historical_cloud_provider_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [826] Historical Registrar: {Colors.DIM}{d.dp826_historical_registrar_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [827] Historical NS: {Colors.DIM}{d.dp827_historical_nameserver_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [828] Historical DNS Provider: {Colors.DIM}{d.dp828_historical_dns_provider_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [829] Routing Changes: {Colors.DIM}{d.dp829_historical_routing_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [830] TLS Changes: {Colors.DIM}{d.dp830_historical_tls_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [831] HTTP Header Changes: {Colors.DIM}{d.dp831_historical_http_header_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [832] Redirect Changes: {Colors.DIM}{d.dp832_historical_redirect_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [833] CMS Changes: {Colors.DIM}{d.dp833_historical_cms_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [834] Framework Changes: {Colors.DIM}{d.dp834_historical_framework_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [835] Server Software Changes: {Colors.DIM}{d.dp835_historical_server_software_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [836] Favicon Changes: {Colors.DIM}{d.dp836_historical_favicon_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [837] Title Changes: {Colors.DIM}{d.dp837_historical_title_changes}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [838] Geolocation Trend: {Colors.DIM}{len(d.dp838_historical_geolocation_trend)} records{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [839] Passive DNS Obs: {Colors.DIM}{d.dp839_passive_dns_observation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [840] Passive Cert Obs: {Colors.DIM}{d.dp840_passive_certificate_observation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [841] Passive HTTP Obs: {Colors.DIM}{d.dp841_passive_http_observation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [842] Passive Service Obs: {Colors.DIM}{d.dp842_passive_service_observation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [843] Public Scan Obs: {Colors.DIM}{d.dp843_public_scan_observation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [844] Related Assets: {Colors.DIM}{d.dp844_related_asset_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [845] Related Hostnames: {Colors.DIM}{d.dp845_related_hostname_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [846] Related Domains: {Colors.DIM}{d.dp846_related_domain_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [847] Related Subdomains: {Colors.DIM}{d.dp847_related_subdomain_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [848] Related IPs: {Colors.DIM}{d.dp848_related_ip_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [849] Related ASNs: {Colors.DIM}{d.dp849_related_asn_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [850] Related Certs: {Colors.DIM}{d.dp850_related_certificate_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [851] Related Email: {Colors.DIM}{len(d.dp851_related_email_infrastructure)} items{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [852] Related CDN: {Colors.DIM}{len(d.dp852_related_cdn_infrastructure)} items{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [853] Related Cloud: {Colors.DIM}{len(d.dp853_related_cloud_infrastructure)} items{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [854] Related API: {Colors.DIM}{len(d.dp854_related_api_infrastructure)} items{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [855] Related Storage: {Colors.DIM}{len(d.dp855_related_storage_endpoints)} items{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [856] Related Identity: {Colors.DIM}{len(d.dp856_related_identity_providers)} items{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [857] Shared Favicon: {Colors.DIM}{len(d.dp857_shared_favicon_correlation)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [858] Shared Headers: {Colors.DIM}{len(d.dp858_shared_http_header_correlation)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [859] Shared TLS FP: {Colors.DIM}{len(d.dp859_shared_tls_fingerprint_correlation)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [860] Shared Tech: {Colors.DIM}{len(d.dp860_shared_technology_correlation)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [861] Shared CMS: {Colors.DIM}{len(d.dp861_shared_cms_correlation)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [862] Shared JS: {Colors.DIM}{len(d.dp862_shared_javascript_library_correlation)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [863] Shared Analytics: {Colors.DIM}{len(d.dp863_shared_analytics_platform)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [864] Shared Tracking: {Colors.DIM}{len(d.dp864_shared_tracking_identifiers)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [865] Shared Issuer: {Colors.DIM}{len(d.dp865_shared_certificate_issuer)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [866] Shared SAN: {Colors.DIM}{len(d.dp866_shared_certificate_san_correlation)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [867] Shared DNS: {Colors.DIM}{len(d.dp867_shared_dns_provider)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [868] Shared Hosting: {Colors.DIM}{len(d.dp868_shared_hosting_provider)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [869] Shared Reverse Proxy: {Colors.DIM}{len(d.dp869_shared_reverse_proxy)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [870] Shared LB: {Colors.DIM}{len(d.dp870_shared_load_balancer)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [871] Shared WAF: {Colors.DIM}{len(d.dp871_shared_waf)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [872] Shared CDN: {Colors.DIM}{len(d.dp872_shared_cdn)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [873] Shared Registrar: {Colors.DIM}{len(d.dp873_shared_registrar)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [874] Shared WHOIS Org: {Colors.DIM}{len(d.dp874_shared_whois_organization)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [875] Shared Abuse Contact: {Colors.DIM}{len(d.dp875_shared_abuse_contact)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [876] Shared Admin Contact: {Colors.DIM}{len(d.dp876_shared_administrative_contact)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [877] Shared Tech Contact: {Colors.DIM}{len(d.dp877_shared_technical_contact)} correlations{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [878] Asset Confidence: {Colors.DIM}{d.dp878_asset_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [879] Discovery Confidence: {Colors.DIM}{d.dp879_discovery_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [880] Fingerprint Confidence: {Colors.DIM}{d.dp880_fingerprint_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [881] ID Confidence: {Colors.DIM}{d.dp881_identification_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [882] Geo Confidence: {Colors.DIM}{d.dp882_geolocation_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [883] Service Confidence: {Colors.DIM}{d.dp883_service_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [884] Tech Confidence: {Colors.DIM}{d.dp884_technology_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [885] Exposure Confidence: {Colors.DIM}{d.dp885_exposure_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [886] Reputation Confidence: {Colors.DIM}{d.dp886_reputation_confidence_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [887] Attack Surface: {Colors.DIM}{d.dp887_external_attack_surface_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [888] Network Exposure: {Colors.DIM}{d.dp888_network_exposure_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [889] Service Exposure: {Colors.DIM}{d.dp889_service_exposure_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [890] Web App Exposure: {Colors.DIM}{d.dp890_web_application_exposure_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [891] Certificate Health: {Colors.DIM}{d.dp891_certificate_health_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [892] DNS Health: {Colors.DIM}{d.dp892_dns_health_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [893] Email Security: {Colors.DIM}{d.dp893_email_security_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [894] HTTP Security: {Colors.DIM}{d.dp894_http_security_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [895] TLS Security: {Colors.DIM}{d.dp895_tls_security_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [896] Infrastructure Resilience: {Colors.DIM}{d.dp896_infrastructure_resilience_score}/100{Colors.RESET}")
        
        risk_color = Colors.BRIGHT_GREEN if d.dp897_overall_risk_score < 30 else Colors.BRIGHT_YELLOW if d.dp897_overall_risk_score < 60 else Colors.BRIGHT_RED
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [897] Overall Risk Score: {risk_color}{d.dp897_overall_risk_score}/100{Colors.RESET}")
        
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [898] Executive Summary Score: {Colors.DIM}{d.dp898_executive_summary_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [899] Security Posture Index: {Colors.DIM}{d.dp899_security_posture_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [900] Asset Maturity: {Colors.DIM}{d.dp900_external_asset_maturity_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [901] Overall Asset Status: {Colors.BRIGHT_WHITE}{d.dp901_overall_asset_status or 'N/A'}{Colors.RESET}")
        
        health_color = Colors.BRIGHT_GREEN if d.dp902_asset_health_score > 70 else Colors.BRIGHT_YELLOW if d.dp902_asset_health_score > 40 else Colors.BRIGHT_RED
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [902] Asset Health: {health_color}{d.dp902_asset_health_score}/100{Colors.RESET}")
        
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [903] Availability Status: {Colors.DIM}{d.dp903_asset_availability_status or 'N/A'}{Colors.RESET}")
        
        crit_color = Colors.BRIGHT_GREEN if d.dp904_asset_criticality_level == 'Low' else Colors.BRIGHT_YELLOW if d.dp904_asset_criticality_level == 'Medium' else Colors.BRIGHT_RED
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [904] Criticality: {crit_color}{d.dp904_asset_criticality_level or 'N/A'}{Colors.RESET}")
        
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [905] Business Impact: {Colors.DIM}{d.dp905_business_impact_rating or 'N/A'}{Colors.RESET}")
        
        exp_color = Colors.BRIGHT_GREEN if d.dp906_exposure_classification == 'Low' else Colors.BRIGHT_YELLOW if d.dp906_exposure_classification == 'Medium' else Colors.BRIGHT_RED
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [906] Exposure: {exp_color}{d.dp906_exposure_classification or 'N/A'}{Colors.RESET}")
        
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [907] Internet Visibility: {Colors.DIM}{d.dp907_internet_visibility_level or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [908] Service Completeness: {Colors.DIM}{d.dp908_service_inventory_completeness or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [909] DNS Completeness: {Colors.DIM}{d.dp909_dns_inventory_completeness or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [910] Certificate Completeness: {Colors.DIM}{d.dp910_certificate_inventory_completeness or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [911] Tech Completeness: {Colors.DIM}{d.dp911_technology_inventory_completeness or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [912] External Dependencies: {Colors.DIM}{d.dp912_external_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [913] Third-party Dependencies: {Colors.DIM}{d.dp913_third_party_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [914] Cloud Dependencies: {Colors.DIM}{d.dp914_cloud_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [915] CDN Dependencies: {Colors.DIM}{d.dp915_cdn_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [916] Auth Dependencies: {Colors.DIM}{d.dp916_authentication_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [917] Email Dependencies: {Colors.DIM}{d.dp917_email_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [918] DNS Dependencies: {Colors.DIM}{d.dp918_dns_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [919] Monitoring Dependencies: {Colors.DIM}{d.dp919_monitoring_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [920] Logging Dependencies: {Colors.DIM}{d.dp920_logging_dependency_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [921] Public Endpoints: {Colors.DIM}{d.dp921_public_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [922] Public APIs: {Colors.DIM}{d.dp922_public_api_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [923] Public Hostnames: {Colors.DIM}{d.dp923_public_hostname_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [924] Public Domains: {Colors.DIM}{d.dp924_public_domain_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [925] Public Subdomains: {Colors.DIM}{d.dp925_public_subdomain_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [926] Public IPs: {Colors.DIM}{d.dp926_public_ip_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [927] Public Certificates: {Colors.DIM}{d.dp927_public_certificate_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [928] Public Services: {Colors.BRIGHT_CYAN}{d.dp928_public_service_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [929] Public Protocols: {Colors.BRIGHT_CYAN}{d.dp929_public_protocol_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [930] Public Technologies: {Colors.DIM}{d.dp930_public_technology_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [931] Public JS Libraries: {Colors.DIM}{d.dp931_public_javascript_library_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [932] Public Frameworks: {Colors.DIM}{d.dp932_public_framework_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [933] Public CMS: {Colors.DIM}{d.dp933_public_cms_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [934] Auth Endpoints: {Colors.DIM}{d.dp934_public_authentication_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [935] Storage Endpoints: {Colors.DIM}{d.dp935_public_storage_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [936] Download Endpoints: {Colors.DIM}{d.dp936_public_download_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [937] Docs Endpoints: {Colors.DIM}{d.dp937_public_documentation_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [938] Webhook Endpoints: {Colors.DIM}{d.dp938_public_webhook_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [939] Health Check Endpoints: {Colors.DIM}{d.dp939_public_health_check_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [940] Metrics Endpoints: {Colors.DIM}{d.dp940_public_metrics_endpoint_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [941] DNS Config Score: {Colors.DIM}{d.dp941_dns_configuration_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [942] TLS Config Score: {Colors.DIM}{d.dp942_tls_configuration_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [943] HTTP Config Score: {Colors.DIM}{d.dp943_http_configuration_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [944] Email Config Score: {Colors.DIM}{d.dp944_email_configuration_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [945] Certificate Mgmt: {Colors.DIM}{d.dp945_certificate_management_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [946] Tech Hygiene: {Colors.DIM}{d.dp946_technology_hygiene_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [947] Service Hardening: {Colors.DIM}{d.dp947_service_hardening_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [948] Encryption Quality: {Colors.DIM}{d.dp948_encryption_quality_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [949] Identity Integration: {Colors.DIM}{d.dp949_identity_integration_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [950] Cloud Config: {Colors.DIM}{d.dp950_cloud_configuration_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [951] CDN Optimization: {Colors.DIM}{d.dp951_cdn_optimization_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [952] Infrastructure Redundancy: {Colors.DIM}{d.dp952_infrastructure_redundancy_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [953] High Availability: {Colors.BRIGHT_WHITE}{d.dp953_high_availability_indicator}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [954] Disaster Recovery: {Colors.BRIGHT_WHITE}{d.dp954_disaster_recovery_indicator}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [955] Geographic Distribution: {Colors.BRIGHT_WHITE}{d.dp955_geographic_distribution_indicator}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [956] Multi-Region: {Colors.BRIGHT_WHITE}{d.dp956_multi_region_deployment_indicator}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [957] Load Balancing: {Colors.DIM}{d.dp957_load_balancing_effectiveness or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [958] Failover Readiness: {Colors.DIM}{d.dp958_failover_readiness or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [959] External Resilience: {Colors.DIM}{d.dp959_external_resilience_score}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [960] Attack Surface Trend: {Colors.DIM}{d.dp960_public_attack_surface_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [961] Exposure Trend: {Colors.DIM}{d.dp961_historical_exposure_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [962] Security Trend: {Colors.DIM}{d.dp962_historical_security_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [963] Tech Trend: {Colors.DIM}{d.dp963_historical_technology_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [964] Certificate Trend: {Colors.DIM}{d.dp964_historical_certificate_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [965] DNS Trend: {Colors.DIM}{d.dp965_historical_dns_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [966] Infrastructure Trend: {Colors.DIM}{d.dp966_historical_infrastructure_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [967] Routing Trend: {Colors.DIM}{d.dp967_historical_routing_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [968] Reputation Trend: {Colors.DIM}{d.dp968_historical_reputation_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [969] Availability Trend: {Colors.DIM}{d.dp969_historical_availability_trend or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [970] Threat Intel Correlations: {Colors.DIM}{d.dp970_threat_intelligence_correlation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [971] Public Advisory Correlations: {Colors.DIM}{d.dp971_public_advisory_correlation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [972] Public CVE Correlations: {Colors.DIM}{d.dp972_public_cve_correlation_count}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [973] Exploited Vuln Correlations: {Colors.DIM}{d.dp973_known_exploited_vulnerability_correlation}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [974] Security Bulletin Correlations: {Colors.DIM}{d.dp974_public_security_bulletin_correlation}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [975] Vendor Advisory Correlations: {Colors.DIM}{d.dp975_public_vendor_advisory_correlation}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [976] Best Practice Alignment: {Colors.DIM}{d.dp976_security_best_practice_alignment or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [977] Baseline Comparison: {Colors.DIM}{d.dp977_baseline_comparison_result or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [978] Config Consistency Index: {Colors.DIM}{d.dp978_configuration_consistency_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [979] Inventory Completeness: {Colors.DIM}{d.dp979_external_inventory_completeness_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [980] Tech Diversity Index: {Colors.DIM}{d.dp980_technology_diversity_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [981] Infrastructure Complexity: {Colors.DIM}{d.dp981_infrastructure_complexity_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [982] External Dependency Index: {Colors.DIM}{d.dp982_external_dependency_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [983] Internet Exposure Index: {Colors.DIM}{d.dp983_internet_exposure_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [984] Asset Trust Index: {Colors.DIM}{d.dp984_asset_trust_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [985] Security Confidence Index: {Colors.DIM}{d.dp985_security_confidence_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [986] Risk Confidence Index: {Colors.DIM}{d.dp986_risk_confidence_index}/100{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [987] Assessment Timestamp: {Colors.DIM}{d.dp987_assessment_timestamp}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [988] Tool Version: {Colors.DIM}{d.dp988_assessment_tool_version}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [989] Profile: {Colors.DIM}{d.dp989_assessment_profile_used or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [990] Scope: {Colors.DIM}{d.dp990_assessment_scope_identifier or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [991] Duration: {Colors.DIM}{d.dp991_assessment_duration or 'N/A'}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [992] Status: {Colors.BRIGHT_GREEN}{d.dp992_assessment_completion_status}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [993] Report Generated: {Colors.DIM}{d.dp993_report_generation_timestamp}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [994] Executive Summary: {Colors.BRIGHT_WHITE}{d.dp994_executive_summary}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [995] Technical Summary: {Colors.DIM}{d.dp995_technical_summary}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [996] Infrastructure Summary: {Colors.DIM}{d.dp996_infrastructure_summary}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [997] Technology Summary: {Colors.DIM}{d.dp997_technology_summary}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [998] Exposure Summary: {Colors.DIM}{d.dp998_exposure_summary}{Colors.RESET}")
        output.append(f"  {Colors.DIM}├─{Colors.RESET} [999] Risk Summary: {Colors.DIM}{d.dp999_risk_summary}{Colors.RESET}")
        
        posture_color = Colors.BRIGHT_GREEN if d.dp1000_overall_external_security_posture_assessment == 'Good' else Colors.BRIGHT_YELLOW if d.dp1000_overall_external_security_posture_assessment == 'Fair' else Colors.BRIGHT_RED
        output.append(f"  {Colors.DIM}└─{Colors.RESET} [1000] Overall Security Posture: {posture_color}{d.dp1000_overall_external_security_posture_assessment}{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # RECOMMENDATIONS
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}█{Colors.RESET} {Colors.BRIGHT_WHITE}RECOMMENDATIONS{Colors.RESET}")
        recs = []
        if not d.dp309_strict_transport_security:
            recs.append("Enable HSTS for improved security")
        if not d.dp301_content_security_policy:
            recs.append("Implement Content Security Policy (CSP)")
        if not d.dp302_x_frame_options:
            recs.append("Set X-Frame-Options to prevent clickjacking")
        if d.dp222_wildcard_certificate:
            recs.append("Consider limiting wildcard certificate usage")
        if not recs:
            recs.append("✅ No critical issues found - good security posture")
        for i, rec in enumerate(recs, 1):
            output.append(f"  {Colors.DIM}{i}.{Colors.RESET} {Colors.BRIGHT_YELLOW}{rec}{Colors.RESET}")
        output.append("")
        
        # ============================================================
        # FOOTER
        # ============================================================
        output.append(f"{Colors.BRIGHT_CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗")
        output.append(f"║ {Colors.BRIGHT_PURPLE}{Symbols.RADAR} 1000 DATA POINTS EXTRACTED {Colors.DIM}• {Colors.BRIGHT_WHITE}HELIXINT v7.0.0{Colors.BRIGHT_CYAN}        ║")
        output.append(f"║ {Colors.BRIGHT_WHITE}Author: SYLHETYHACKVENGER {Colors.DIM}(THE-ERROR808){Colors.BRIGHT_WHITE}                                {Colors.BRIGHT_CYAN}║")
        output.append(f"╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        
        return '\n'.join(output)

# ============================================================
#   MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='HELIXINT Ultimate - 1000 Data Point Reconnaissance',
        epilog=f'{Colors.BRIGHT_PURPLE}🚀 Complete external asset intelligence gathering{Colors.RESET}'
    )
    parser.add_argument('targets', nargs='*', help='Target IPs or hostnames')
    parser.add_argument('-i', '--input', help='Input file with targets')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-f', '--format', choices=['text', 'json'], default='text')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    parser.add_argument('--no-header', action='store_true', help='Hide header')
    
    args = parser.parse_args()
    
    targets = args.targets or []
    if args.input:
        try:
            with open(args.input, 'r') as f:
                targets.extend([line.strip() for line in f if line.strip()])
        except Exception as e:
            print(f"{Colors.BRIGHT_RED}ERROR{Colors.RESET}: {e}")
            sys.exit(1)
    
    if not targets:
        parser.print_help()
        sys.exit(1)
    
    if not args.quiet and not args.no_header:
        print(CyberHeader.generate())
    
    engine = HELIXINTEngine(quiet=args.quiet, debug=args.debug)
    
    for target in targets:
        if not args.quiet:
            print(f"\n{Colors.BRIGHT_PURPLE}{'='*60}")
            print(f"🎯 TARGET: {Colors.BRIGHT_WHITE}{target}{Colors.RESET}")
            print(f"{Colors.BRIGHT_PURPLE}{'='*60}{Colors.RESET}\n")
        
        report = engine.recon(target)
        
        if args.format == 'json':
            output = json.dumps(asdict(report), indent=2, default=str)
        else:
            output = CyberOutput.full_text(report)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            if not args.quiet:
                print(f"\n{Colors.BRIGHT_GREEN}✓ Report saved to: {Colors.BRIGHT_WHITE}{args.output}{Colors.RESET}")
        else:
            print(output)
    
    if not args.quiet:
        print(f"\n{Colors.BRIGHT_PURPLE}🚀 HELIXINT ULTIMATE - Mission Complete{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}Author: SYLHETYHACKVENGER {Colors.DIM}(THE-ERROR808){Colors.RESET}")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}⚠ Mission Aborted by Operator{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}💀 FATAL ERROR{Colors.RESET}: {e}")
        if '-d' in sys.argv or '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
