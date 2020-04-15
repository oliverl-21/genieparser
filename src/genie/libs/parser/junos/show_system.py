"""show_system.py

JunOS parsers for the following show commands:
    - 'show system buffers'
"""

# python
import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Optional


class ShowSystemBufferSchema(MetaParser):
    """ Schema for:
            - 'show system buffers'
    """

    schema = {
        "memory-statistics": {
            "cached-bytes": str,
            "cached-jumbo-clusters-16k": str,
            "cached-jumbo-clusters-4k": str,
            "cached-jumbo-clusters-9k": str,
            "cached-mbuf-clusters": str,
            "cached-mbufs": str,
            "cluster-failures": str,
            "current-bytes-in-use": str,
            "current-jumbo-clusters-16k": str,
            "current-jumbo-clusters-4k": str,
            "current-jumbo-clusters-9k": str,
            "current-mbuf-clusters": str,
            "current-mbufs": str,
            "io-initiated": str,
            "jumbo-cluster-failures-16k": str,
            "jumbo-cluster-failures-4k": str,
            "jumbo-cluster-failures-9k": str,
            "max-jumbo-clusters-16k": str,
            "max-jumbo-clusters-4k": str,
            "max-jumbo-clusters-9k": str,
            "max-mbuf-clusters": str,
            "mbuf-failures": str,
            "packet-count": str,
            "packet-failures": str,
            "packet-free": str,
            "sfbuf-requests-delayed": str,
            "sfbuf-requests-denied": str,
            "total-bytes": str,
            "total-jumbo-clusters-16k": str,
            "total-jumbo-clusters-4k": str,
            "total-jumbo-clusters-9k": str,
            "total-mbuf-clusters": str,
            "total-mbufs": str
        }
    }


class ShowSystemBuffer(ShowSystemBufferSchema):
    """ Parser for:
            - 'show system buffers'
    """

    cli_command = "show system buffers"

    def cli(self, node_id=None, output=None):
        if not output:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # init vars
        ret_dict = {}

        # 588/2142/2730 mbufs in use (current/cache/total)
        p1 = re.compile(r'^(?P<current_mbufs>\S+)/(?P<cached_mbufs>\S+)/'
        r'(?P<total_mbufs>\S+) +mbufs +in +use +\(current/cache/total\)$')

        # 516/714/1230/124756 mbuf clusters in use (current/cache/total/max)
        p2 = re.compile(r'^(?P<current_mbuf_clusters>\S+)/(?P<cached_mbuf_clusters>\S+)'
        r'/(?P<total_mbuf_clusters>\S+)/(?P<max_mbuf_clusters>\S+) +mbuf +clusters'
        r' +in use +\(current/cache/total/max\)$')

        # 513/499 mbuf+clusters out of packet secondary zone in use (current/cache)
        p3 = re.compile(r'^(?P<packet_count>\S+)/(?P<packet_free>\S+) +mbuf\+clusters'
        r' +out +of +packet +secondary +zone +in +use +\(current/cache\)$')

        # 0/2/2/62377 4k (page size) jumbo clusters in use (current/cache/total/max)
        p4 = re.compile(r'^(?P<current_jumbo_clusters_4k>\S+)/'
        r'(?P<cached_jumbo_clusters_4k>\S+)/(?P<total_jumbo_clusters_4k>\S+)/'
        r'(?P<max_jumbo_clusters_4k>\S+) +4k +\(page +size\) +jumbo +clusters +in'
        r' +use +\(current/cache/total/max\)$')

        # 0/0/0/18482 9k (page size) jumbo clusters in use (current/cache/total/max)
        p5 = re.compile(r'^(?P<current_jumbo_clusters_9k>\S+)/'
        r'(?P<cached_jumbo_clusters_9k>\S+)/(?P<total_jumbo_clusters_9k>\S+)/'
        r'(?P<max_jumbo_clusters_9k>\S+) +9k +\(page +size\) +jumbo +clusters +in'
        r' +use +\(current/cache/total/max\)$')

        # 0/0/0/10396 16k (page size) jumbo clusters in use (current/cache/total/max)
        p6 = re.compile(r'^(?P<current_jumbo_clusters_16k>\S+)/'
        r'(?P<cached_jumbo_clusters_16k>\S+)/(?P<total_jumbo_clusters_16k>\S+)/'
        r'(?P<max_jumbo_clusters_16k>\S+) +16k +\(page +size\) +jumbo +clusters'
        r' +in +use +\(current/cache/total/max\)$')

        # 1179K/1971K/3150K bytes allocated to network (current/cache/total)
        p7 =re.compile(r'^(?P<current_bytes_in_use>\S+)K/(?P<cached_bytes>\S+)K/'
        r'(?P<total_bytes>\S+)K +bytes +allocated +to +network +\(current/cache/total\)$')

        # 0/0/0 requests for mbufs denied (mbufs/clusters/mbuf+clusters)
        p8 = re.compile(r'^(?P<mbuf_failures>\S+)/(?P<cluster_failures>\S+)/'
        r'(?P<packet_failures>\S+) +requests +for +mbufs +denied +\(mbufs/clusters/mbuf\+clusters\)$')

        # 0/0/0 requests for jumbo clusters denied (4k/9k/16k)
        p9 =re.compile(r'^(?P<jumbo_cluster_failures_4k>\S+)/(?P<jumbo_cluster_failures_9k>\S+)'
        r'/(?P<jumbo_cluster_failures_16k>\S+) +requests +for +jumbo +clusters +denied +\(4k/9k/16k\)$')

        # 0 requests for sfbufs denied
        p10 = re.compile(r'^(?P<sfbuf_requests_denied>\S+) +requests +for +sfbufs'
        r' +denied$')

        # 0 requests for sfbufs delayed
        p11 = re.compile(r'^(?P<sfbuf_requests_delayed>\S+) +requests +for'
        r' +sfbufs +delayed$')

        # 0 requests for I/O initiated by sendfile
        p12 = re.compile(r'^(?P<io_initiated>\S+) +requests +for +I/O +initiated'
        r' +by +sendfile$')

        for line in out.splitlines():
            line = line.strip()

            # 588/2142/2730 mbufs in use (current/cache/total)
            m = p1.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 516/714/1230/124756 mbuf clusters in use (current/cache/total/max)
            m = p2.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 513/499 mbuf+clusters out of packet secondary zone in use (current/cache)
            m = p3.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0/2/2/62377 4k (page size) jumbo clusters in use (current/cache/total/max)
            m = p4.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0/0/0/18482 9k (page size) jumbo clusters in use (current/cache/total/max)
            m = p5.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0/0/0/10396 16k (page size) jumbo clusters in use (current/cache/total/max)
            m = p6.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 1179K/1971K/3150K bytes allocated to network (current/cache/total)
            m = p7.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0/0/0 requests for mbufs denied (mbufs/clusters/mbuf+clusters)
            m = p8.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0/0/0 requests for jumbo clusters denied (4k/9k/16k)
            m = p9.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0 requests for sfbufs denied
            m = p10.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0 requests for sfbufs delayed
            m = p11.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

            # 0 requests for I/O initiated by sendfile
            m = p12.match(line)
            if m:
                group = m.groupdict()
                entry = ret_dict.setdefault("memory-statistics", {})
                for group_key, group_value in group.items():
                    entry_key = group_key.replace('_','-')
                    entry[entry_key] = group_value
                continue

        return ret_dict

class ShowSystemStatisticsSchema(MetaParser):
    """ Schema for:
            * show system statistics
    """

    schema = {
        "statistics": [
            {
                "ah": {
                    "bytes-in": str,
                    "bytes-out": str,
                    "crypto-processing-failure": str,
                    "packets-blocked-due-to-policy": str,
                    "packets-dropped-as-bad-authentication-detected": str,
                    "packets-dropped-as-larger-than-ip-maxpacket": str,
                    "packets-dropped-as-protocol-unsupported": str,
                    "packets-dropped-due-to-bad-authentication-length": str,
                    "packets-dropped-due-to-bad-kcr": str,
                    "packets-dropped-due-to-invalid-tdb": str,
                    "packets-dropped-due-to-no-tdb": str,
                    "packets-dropped-due-to-no-transform": str,
                    "packets-dropped-due-to-queue-full": str,
                    "packets-in": str,
                    "packets-out": str,
                    "packets-shorter-than-header-shows": str,
                    "possible-replay-packets-detected": str,
                    "replay-counter-wrap": str,
                    "tunnel-sanity-check-failures": str
                },
                "arp": {
                    "arp-iri-cnt": str,
                    "arp-iri-drop": str,
                    "arp-iri-max": str,
                    "arp-mgt-cnt": str,
                    "arp-mgt-drop": str,
                    "arp-mgt-max": str,
                    "arp-packets-are-dropped-as-driver-call-failed": str,
                    "arp-packets-are-dropped-as-nexthop-allocation-failed": str,
                    "arp-packets-are-dropped-as-source-is-not-validated": str,
                    "arp-packets-are-dropped-from-peer-vrrp": str,
                    "arp-packets-are-rejected-as-target-ip-arp-resolve-is-in-progress": str,
                    "arp-packets-received-from-peer-vrrp-router-and-discarded": str,
                    "arp-packets-rejected-as-family-is-configured-with-deny-arp": str,
                    "arp-probe-for-proxy-address-reachable-from-the-incoming-interface": str,
                    "arp-public-cnt": str,
                    "arp-public-drop": str,
                    "arp-public-max": str,
                    "arp-replies-are-rejected-as-source-and-destination-is-same": str,
                    "arp-replies-received": str,
                    "arp-replies-sent": str,
                    "arp-request-discarded-for-vrrp-source-address": str,
                    "arp-requests-received": str,
                    "arp-requests-sent": str,
                    "arp-response-packets-are-rejected-on-mace-icl-interface": str,
                    "arp-system-drop": str,
                    "arp-system-max": str,
                    "datagrams-for-an-address-not-on-the-interface": str,
                    "datagrams-for-non-ip-protocol": str,
                    "datagrams-received": str,
                    "datagrams-which-were-not-for-me": str,
                    "datagrams-with-a-broadcast-source-address": str,
                    "datagrams-with-bad-hardware-address-length": str,
                    "datagrams-with-bad-protocol-address-length": str,
                    "datagrams-with-bogus-interface": str,
                    "datagrams-with-incorrect-length": str,
                    "datagrams-with-multicast-source-address": str,
                    "datagrams-with-multicast-target-address": str,
                    "datagrams-with-my-own-hardware-address": str,
                    "datagrams-with-source-address-duplicate-to-mine": str,
                    "datagrams-with-unsupported-opcode": str,
                    "grat-arp-packets-are-ignored-as-mac-address-is-not-changed": str,
                    "new-requests-on-unnumbered-interfaces": str,
                    "packets-discarded-waiting-for-resolution": str,
                    "packets-sent-after-waiting-for-resolution": str,
                    "proxy-arp-request-discarded-as-source-ip-is-a-proxy-target": str,
                    "proxy-requests-not-proxied": str,
                    "received-proxy-requests": str,
                    "replies-from-unnumbered-interface-with-non-subnetted-donor": str,
                    "replies-from-unnumbered-interfaces": str,
                    "requests-dropped-due-to-interface-deletion": str,
                    "requests-dropped-during-retry": str,
                    "requests-dropped-on-entry": str,
                    "requests-for-memory-denied": str,
                    "requests-on-unnumbered-interface-with-non-subnetted-donor": str,
                    "requests-on-unnumbered-interfaces": str,
                    "resolution-request-dropped": str,
                    "resolution-request-received": str,
                    "restricted-proxy-requests": str,
                    "restricted-proxy-requests-not-proxied": str,
                    "self-arp-request-packet-received-on-irb-interface": str,
                    "unrestricted-proxy-requests": str
                },
                "clnl": {
                    "address-fields-were-not-reasonable": str,
                    "bad-version-packets": str,
                    "er-pdu-generation-failure": str,
                    "error-pdu-rate-drops": str,
                    "forwarded-packets": str,
                    "fragmentation-prohibited": str,
                    "fragments-discarded": str,
                    "fragments-sent": str,
                    "fragments-timed-out": str,
                    "mcopy-failure": str,
                    "no-free-memory-in-socket-buffer": str,
                    "non-forwarded-packets": str,
                    "output-packets-discarded": str,
                    "packets-delivered": str,
                    "packets-destined-to-dead-nexthop": str,
                    "packets-discarded-due-to-no-route": str,
                    "packets-fragmented": str,
                    "packets-reconstructed": str,
                    "packets-with-bad-checksum": str,
                    "packets-with-bad-header-length": str,
                    "packets-with-bogus-sdl-size": str,
                    "sbappend-failure": str,
                    "segment-information-forgotten": str,
                    "send-packets-discarded": str,
                    "too-small-packets": str,
                    "total-clnl-packets-received": str,
                    "total-packets-sent": str,
                    "unknown-or-unsupported-protocol-packets": str
                },
                "esis": {
                    "iso-family-not-configured": str,
                    "pdus-received-with-bad-checksum": str,
                    "pdus-received-with-bad-type-field": str,
                    "pdus-received-with-bad-version-number": str,
                    "pdus-with-bad-header-length": str,
                    "pdus-with-bogus-sdl-size": str,
                    "pdus-with-unknown-or-unsupport-protocol": str,
                    "short-pdus-received": str,
                    "total-esis-packets-received": str,
                    "total-packets-consumed-by-protocol": str
                },
                "esp": {
                    "esp-bytes-in": str,
                    "esp-bytes-out": str,
                    "esp-crypto-processing-failure": str,
                    "esp-packets-blocked-due-to-policy": str,
                    "esp-packets-dropped-as-bad-authentication-detected": str,
                    "esp-packets-dropped-as-bad-encryption-detected": str,
                    "esp-packets-dropped-as-bad-ilen": str,
                    "esp-packets-dropped-as-invalid-tdb": str,
                    "esp-packets-dropped-as-larger-than-ip-maxpacket": str,
                    "esp-packets-dropped-as-protocol-not-supported": str,
                    "esp-packets-dropped-due-to-bad-kcr": str,
                    "esp-packets-dropped-due-to-no-tdb": str,
                    "esp-packets-dropped-due-to-no-transform": str,
                    "esp-packets-dropped-due-to-queue-full": str,
                    "esp-packets-in": str,
                    "esp-packets-out": str,
                    "esp-packets-shorter-than-header-shows": str,
                    "esp-possible-replay-packets-detected": str,
                    "esp-replay-counter-wrap": str,
                    "esp-tunnel-sanity-check-failures": str
                },
                "ethoamcfm": {
                    "flood-requests-dropped": str,
                    "flood-requests-forwarded-to-pfe": str,
                    "input-packets-drop-bad-interface-state": str,
                    "output-packets-drop-bad-interface-state": str,
                    "packets-sent": str,
                    "received-packets-forwarded": str,
                    "total-packets-received": str,
                    "total-packets-transmitted": str
                },
                "ethoamlfm": {
                    "input-packets-drop-bad-interface-state": str,
                    "output-packets-drop-bad-interface-state": str,
                    "packets-sent": str,
                    "received-packets-forwarded": str,
                    "total-packets-received": str,
                    "total-packets-transmitted": str
                },
                "icmp": {
                    "calls-to-icmp-error": str,
                    "drops-due-to-rate-limit": str,
                    "echo-drops-with-broadcast-or-multicast-destinaton-address": str,
                    "errors-not-generated-because-old-message-was-icmp": str,
                    "histogram": [
                        {
                            "destination-unreachable": str,
                            "icmp-echo": str,
                            "icmp-echo-reply": str,
                            "time-exceeded": str,
                            "type-of-histogram": str
                        }
                    ],
                    "message-responses-generated": str,
                    "messages-less-than-the-minimum-length": str,
                    "messages-with-bad-checksum": str,
                    "messages-with-bad-code-fields": str,
                    "messages-with-bad-length": str,
                    "messages-with-bad-source-address": str,
                    "timestamp-drops-with-broadcast-or-multicast-destination-address": str
                },
                "icmp6": {
                    "address-unreachable": str,
                    "administratively-prohibited": str,
                    "bad-checksums": str,
                    "beyond-scope": str,
                    "calls-to-icmp6-error": str,
                    "erroneous-header-field": str,
                    "errors-not-generated-because-old-message-was-icmp-error": str,
                    "errors-not-generated-because-rate-limitation": str,
                    "histogram-of-error-messages-to-be-generated": str,
                    "icmp6-message-responses-generated": str,
                    "icmp6-messages-with-bad-code-fields": str,
                    "icmp6-messages-with-bad-length": str,
                    "input-histogram": {
                        "histogram-type": str,
                        "neighbor-advertisement": str,
                        "neighbor-solicitation": str,
                        "router-advertisement-icmp6-packets": str,
                        "router-solicitation-icmp6-packets": str,
                        "time-exceeded-icmp6-packets": str,
                        "unreachable-icmp6-packets": str
                    },
                    "messages-less-than-minimum-length": str,
                    "messages-with-too-many-nd-options": str,
                    "nd-iri-cnt": str,
                    "nd-iri-drop": str,
                    "nd-iri-max": str,
                    "nd-mgt-cnt": str,
                    "nd-mgt-drop": str,
                    "nd-mgt-max": str,
                    "nd-public-cnt": str,
                    "nd-public-drop": str,
                    "nd-public-max": str,
                    "nd-system-drop": str,
                    "nd-system-max": str,
                    "nd6-dad-proxy-conflicts": str,
                    "nd6-dad-proxy-eqmac-drop": str,
                    "nd6-dad-proxy-nomac-drop": str,
                    "nd6-dad-proxy-requests": str,
                    "nd6-dad-proxy-resolve-cnt": str,
                    "nd6-dup-proxy-responses": str,
                    "nd6-ndp-proxy-requests": str,
                    "nd6-ndp-proxy-resolve-cnt": str,
                    "nd6-ndp-proxy-responses": str,
                    "nd6-requests-dropped-during-retry": str,
                    "nd6-requests-dropped-on-entry": str,
                    "no-route": str,
                    "output-histogram": {},
                    "packet-too-big": str,
                    "port-unreachable": str,
                    "protocol-name": str,
                    "redirect": str,
                    "time-exceed-reassembly": str,
                    "time-exceed-transit": str,
                    "unknown": str,
                    "unrecognized-next-header": str,
                    "unrecognized-option": str
                },
                "igmp": {
                    "membership-queries-received": str,
                    "membership-queries-received-with-invalid-fields": str,
                    "membership-reports-received": str,
                    "membership-reports-received-for-groups-to-which-we-belong": str,
                    "membership-reports-received-with-invalid-fields": str,
                    "membership-reports-sent": str,
                    "messages-received": str,
                    "messages-received-with-bad-checksum": str,
                    "messages-received-with-too-few-bytes": str
                },
                "ip": {
                    "bad-header-checksums": str,
                    "datagrams-that-can-not-be-fragmented": str,
                    "fragments-created": str,
                    "fragments-dropped-after-timeout": str,
                    "fragments-dropped-due-to-outofspace-or-dup": str,
                    "fragments-dropped-due-to-queueoverflow": str,
                    "fragments-received": str,
                    "incoming-rawip-packets-dropped-no-socket-buffer": str,
                    "incoming-ttpoip-packets-dropped": str,
                    "incoming-ttpoip-packets-received": str,
                    "incoming-virtual-node-packets-delivered": str,
                    "loose-source-and-record-route-options": str,
                    "multicast-packets-dropped": str,
                    "option-packets-dropped-due-to-rate-limit": str,
                    "outgoing-ttpoip-packets-dropped": str,
                    "outgoing-ttpoip-packets-sent": str,
                    "output-datagrams-fragmented": str,
                    "output-packets-discarded-due-to-no-route": str,
                    "output-packets-dropped-due-to-no-bufs": str,
                    "packets-destined-to-dead-next-hop": str,
                    "packets-dropped": str,
                    "packets-for-this-host": str,
                    "packets-for-unknown-or-unsupported-protocol": str,
                    "packets-forwarded": str,
                    "packets-not-forwardable": str,
                    "packets-reassembled-ok": str,
                    "packets-received": str,
                    "packets-sent-from-this-host": str,
                    "packets-sent-with-fabricated-ip-header": str,
                    "packets-used-first-nexthop-in-ecmp-unilist": str,
                    "packets-with-bad-options": str,
                    "packets-with-data-length-less-than-headerlength": str,
                    "packets-with-data-size-less-than-datalength": str,
                    "packets-with-header-length-less-than-data-size": str,
                    "packets-with-incorrect-version-number": str,
                    "packets-with-options-handled-without-error": str,
                    "packets-with-size-smaller-than-minimum": str,
                    "record-route-options": str,
                    "redirects-sent": str,
                    "router-alert-options": str,
                    "strict-source-and-record-route-options": str,
                    "timestamp-and-address-options": str,
                    "timestamp-and-prespecified-address-options": str,
                    "timestamp-options": str,
                    "transit-re-packets-dropped-on-mgmt-interface": str
                },
                "ip6": {
                    "duplicate-or-out-of-space-fragments-dropped": str,
                    "failures-of-source-address-selection": str,
                    "forward-cache-hit": str,
                    "forward-cache-miss": str,
                    "fragments-that-exceeded-limit": str,
                    "header-type": [
                        {
                            "globals": str,
                            "header-for-source-address-selection": str,
                            "link-locals": str
                        }
                    ],
                    "histogram": str,
                    "ip6-datagrams-that-can-not-be-fragmented": str,
                    "ip6-fragments-created": str,
                    "ip6-fragments-dropped-after-timeout": str,
                    "ip6-fragments-received": str,
                    "ip6-option-packets-dropped-due-to-rate-limit": str,
                    "ip6-output-datagrams-fragmented": str,
                    "ip6-output-packets-discarded-due-to-no-route": str,
                    "ip6-output-packets-dropped-due-to-no-bufs": str,
                    "ip6-packets-destined-to-dead-next-hop": str,
                    "ip6-packets-dropped": str,
                    "ip6-packets-for-this-host": str,
                    "ip6-packets-forwarded": str,
                    "ip6-packets-not-forwardable": str,
                    "ip6-packets-reassembled-ok": str,
                    "ip6-packets-sent-from-this-host": str,
                    "ip6-packets-sent-with-fabricated-ip-header": str,
                    "ip6-packets-with-bad-options": str,
                    "ip6-packets-with-incorrect-version-number": str,
                    "ip6-packets-with-size-smaller-than-minimum": str,
                    "ip6-redirects-sent": str,
                    "ip6nh-icmp6": str,
                    "ip6nh-ospf": str,
                    "ip6nh-tcp": str,
                    "ip6nh-udp": str,
                    "multicast-packets-which-we-do-not-join": str,
                    "packets-discarded-due-to-too-may-headers": str,
                    "packets-dropped-due-to-bad-protocol": str,
                    "packets-that-violated-scope-rules": str,
                    "packets-whose-headers-are-not-continuous": str,
                    "packets-with-datasize-less-than-data-length": str,
                    "transit-re-packet-dropped-on-mgmt-interface": str,
                    "tunneling-packets-that-can-not-find-gif": str
                },
                "ipcomp": {
                    "ipcomp-bytes-in": str,
                    "ipcomp-bytes-out": str,
                    "ipcomp-crypto-processing-failure": str,
                    "ipcomp-packets-blocked-due-to-policy": str,
                    "ipcomp-packets-dropped-as-invalid-tdb": str,
                    "ipcomp-packets-dropped-as-larger-than-ip-maxpacket": str,
                    "ipcomp-packets-dropped-as-protocol-not-supported": str,
                    "ipcomp-packets-dropped-due-to-bad-kcr": str,
                    "ipcomp-packets-dropped-due-to-no-tdb": str,
                    "ipcomp-packets-dropped-due-to-no-transform": str,
                    "ipcomp-packets-dropped-due-to-queue-full": str,
                    "ipcomp-packets-in": str,
                    "ipcomp-packets-out": str,
                    "ipcomp-packets-shorter-than-header-shows": str,
                    "ipcomp-replay-counter-wrap": str,
                    "packets-sent-uncompressed-threshold": str,
                    "packets-sent-uncompressed-useless": str
                },
                "ipsec": {
                    "cluster-coalesced-during-clone": str,
                    "cluster-copied-during-clone": str,
                    "inbound-packets-violated-process-security-policy": str,
                    "invalid-outbound-packets": str,
                    "mbuf-coalesced-during-clone": str,
                    "mbuf-inserted-during-makespace": str,
                    "outbound-packets-failed-due-to-insufficient-memory": str,
                    "outbound-packets-violated-process-security-policy": str,
                    "outbound-packets-with-bundled-sa": str,
                    "outbound-packets-with-no-route": str,
                    "outbound-packets-with-no-sa-available": str
                },
                "ipsec6": {
                    "cluster-coalesced-during-clone": str,
                    "cluster-copied-during-clone": str,
                    "inbound-packets-violated-process-security-policy": str,
                    "invalid-outbound-packets": str,
                    "mbuf-coalesced-during-clone": str,
                    "mbuf-inserted-during-makespace": str,
                    "outbound-packets-failed-due-to-insufficient-memory": str,
                    "outbound-packets-violated-process-security-policy": str,
                    "outbound-packets-with-bundled-sa": str,
                    "outbound-packets-with-no-route": str,
                    "outbound-packets-with-no-sa-available": str
                },
                "mpls": {
                    "after-tagging-packets-can-not-fit-link-mtu": str,
                    "lsp-ping-packets": str,
                    "packets-dropped-at-mpls-socket-send": str,
                    "packets-dropped-at-p2mp-cnh-output": str,
                    "packets-dropped-due-to-ifl-down": str,
                    "packets-forwarded-at-mpls-socket-send": str,
                    "packets-with-header-too-small": str,
                    "packets-with-ipv4-explicit-null-checksum-errors": str,
                    "packets-with-ipv4-explicit-null-tag": str,
                    "packets-with-router-alert-tag": str,
                    "packets-with-tag-encoding-error": str,
                    "packets-with-ttl-expired": str,
                    "total-mpls-packets-received": str
                },
                "pfkey": {
                    "bytes-sent-from-userland": str,
                    "bytes-sent-to-userland": str,
                    "incoming-messages-with-memory-allocation-failure": str,
                    "input-histogram": {
                        "add": str,
                        "dump": str,
                        "reserved": str
                    },
                    "messages-too-short": str,
                    "messages-toward-all-sockets": str,
                    "messages-toward-registered-sockets": str,
                    "messages-toward-single-socket": str,
                    "messages-with-duplicate-extension": str,
                    "messages-with-invalid-address-extension": str,
                    "messages-with-invalid-extension-type": str,
                    "messages-with-invalid-length-field": str,
                    "messages-with-invalid-message-type-field": str,
                    "messages-with-invalid-sa-type": str,
                    "messages-with-invalid-version-field": str,
                    "outgoing-messages-with-memory-allocation-failure": str,
                    "output-histogram": {},
                    "requests-sent-from-userland": str,
                    "requests-sent-to-userland": str
                },
                "raw-interface": {
                    "dialer-packets-received": str,
                    "dialer-packets-transmitted": str,
                    "faboam-packets-dropped": str,
                    "faboam-packets-received": str,
                    "faboam-packets-transmitted": str,
                    "fibre-channel-packets-dropped": str,
                    "fibre-channel-packets-received": str,
                    "fibre-channel-packets-transmitted": str,
                    "fip-packets-dropped": str,
                    "fip-packets-received": str,
                    "fip-packets-transmitted": str,
                    "igmpl2-packets-received": str,
                    "igmpl2-packets-transmitted": str,
                    "input-drops-due-to-bogus-protocol": str,
                    "input-drops-due-to-no-mbufs-available": str,
                    "input-drops-due-to-no-socket": str,
                    "input-drops-due-to-no-space-in-socket": str,
                    "isdn-packets-received": str,
                    "isdn-packets-transmitted": str,
                    "lacp-packets-dropped": str,
                    "lacp-packets-received": str,
                    "lacp-packets-transmitted": str,
                    "mldl2-packets-received": str,
                    "mldl2-packets-transmitted": str,
                    "mpu-packets-received": str,
                    "mpu-packets-transmitted": str,
                    "output-drops-due-to-transmit-error": str,
                    "ppoe-packets-transmitted": str,
                    "ppp-packets-received-from-jppd": str,
                    "ppp-packets-received-from-pppd": str,
                    "ppp-packets-transmitted-to-jppd": str,
                    "ppp-packets-transmitted-to-pppd": str,
                    "pppoe-packets-received": str,
                    "raw-packets-transmitted": str,
                    "stp-packets-dropped": str,
                    "stp-packets-received": str,
                    "stp-packets-transmitted": str,
                    "vccp-packets-dropped": str,
                    "vccp-packets-received": str,
                    "vccp-packets-transmitted": str
                },
                "rdp": {
                    "acks-received": str,
                    "acks-sent": str,
                    "closes": str,
                    "connects": str,
                    "input-packets": str,
                    "keepalives-received": str,
                    "keepalives-sent": str,
                    "output-packets": str,
                    "packets-discarded-due-to-bad-sequence-number": str,
                    "packets-discarded-for-bad-checksum": str,
                    "packets-dropped-due-to-full-socket-buffers": str,
                    "packets-dropped-full-repl-sock-buf": str,
                    "refused-connections": str,
                    "retransmits": str
                },
                "tcp": {
                    "aborted": str,
                    "ack-header-predictions": str,
                    "acks-bytes": str,
                    "acks-sent-in-response-but-not-exact-rsts": str,
                    "acks-sent-in-response-to-syns-on-established-connections": str,
                    "attempts": str,
                    "bad-connection-attempts": str,
                    "badack": str,
                    "bucket-overflow": str,
                    "byte-retransmits": str,
                    "bytes": str,
                    "cache-overflow": str,
                    "completed": str,
                    "connection-accepts": str,
                    "connection-requests": str,
                    "connections-closed": str,
                    "connections-dropped-by-persist-timeout": str,
                    "connections-dropped-by-retransmit-timeout": str,
                    "connections-established": str,
                    "connections-updated-rtt-on-close": str,
                    "connections-updated-ssthresh-on-close": str,
                    "connections-updated-variance-on-close": str,
                    "cookies-received": str,
                    "cookies-sent": str,
                    "data-packet-header-predictions": str,
                    "data-packets-bytes": str,
                    "dropped": str,
                    "drops": str,
                    "duplicate-in-bytes": str,
                    "dupsyn": str,
                    "embryonic-connections-dropped": str,
                    "icmp-packets-ignored": str,
                    "in-sequence-bytes": str,
                    "keepalive-connections-dropped": str,
                    "keepalive-probes-sent": str,
                    "keepalive-timeouts": str,
                    "listen-queue-overflows": str,
                    "out-of-order-in-bytes": str,
                    "out-of-sequence-segment-drops": str,
                    "outgoing-segments-dropped": str,
                    "packets-received-after-close": str,
                    "packets-received-in-sequence": str,
                    "persist-timeouts": str,
                    "rcv-packets-dropped": str,
                    "rcv-packets-dropped-due-to-bad-address": str,
                    "received-acks": str,
                    "received-acks-for-unsent-data": str,
                    "received-completely-duplicate-packet": str,
                    "received-discarded-because-packet-too-short": str,
                    "received-discarded-for-bad-checksum": str,
                    "received-discarded-for-bad-header-offset": str,
                    "received-duplicate-acks": str,
                    "received-old-duplicate-packets": str,
                    "received-out-of-order-packets": str,
                    "received-packets-of-data-after-window": str,
                    "received-packets-with-some-dupliacte-data": str,
                    "received-window-probes": str,
                    "received-window-update-packets": str,
                    "reset": str,
                    "retransmit-timeouts": str,
                    "retransmitted": str,
                    "retransmitted-bytes": str,
                    "rst-packets": str,
                    "sack-opitions-sent": str,
                    "sack-options-received": str,
                    "sack-recovery-episodes": str,
                    "sack-scoreboard-overflow": str,
                    "segment-retransmits": str,
                    "segments-updated-rtt": str,
                    "send-packets-dropped": str,
                    "sent-ack-only-packets": str,
                    "sent-control-packets": str,
                    "sent-data-packets": str,
                    "sent-data-packets-retransmitted": str,
                    "sent-packets-delayed": str,
                    "sent-resends-by-mtu-discovery": str,
                    "sent-urg-only-packets": str,
                    "sent-window-probe-packets": str,
                    "sent-window-update-packets": str,
                    "some-duplicate-in-bytes": str,
                    "stale": str,
                    "syncache-entries-added": str,
                    "unreach": str,
                    "zone-failures": str
                },
                "tnp": {
                    "broadcast-packets-received": str,
                    "broadcast-packets-sent": str,
                    "control-packets-received": str,
                    "control-packets-sent": str,
                    "fragment-reassembly-queue-flushes": str,
                    "fragmented-packets-received": str,
                    "fragmented-packets-sent": str,
                    "hello-packets-received": str,
                    "hello-packets-sent": str,
                    "input-packets-discarded-with-no-protocol": str,
                    "packets-of-version-unspecified-received": str,
                    "packets-of-version-unspecified-sent": str,
                    "packets-of-version1-received": str,
                    "packets-of-version1-sent": str,
                    "packets-of-version2-received": str,
                    "packets-of-version2-sent": str,
                    "packets-of-version3-received": str,
                    "packets-of-version3-sent": str,
                    "packets-sent-with-unknown-protocol": str,
                    "packets-with-tnp-src-address-collision-received": str,
                    "rdp-packets-received": str,
                    "rdp-packets-sent": str,
                    "received-fragments-dropped": str,
                    "received-hello-packets-dropped": str,
                    "sent-fragments-dropped": str,
                    "sent-hello-packets-dropped": str,
                    "tunnel-packets-received": str,
                    "tunnel-packets-sent": str,
                    "udp-packets-received": str,
                    "udp-packets-sent": str,
                    "unicast-packets-received": str,
                    "unicast-packets-sent": str
                },
                "ttp": {
                    "arp-l3-packets-received": str,
                    "clnp-l3-packets-received": str,
                    "cyclotron-cycle-l3-packets-received": str,
                    "cyclotron-send-l3-packets-received": str,
                    "input-packets-could-not-get-buffer": str,
                    "input-packets-for-which-route-lookup-is-bypassed": str,
                    "input-packets-tlv-dropped": str,
                    "input-packets-with-bad-af": str,
                    "input-packets-with-bad-tlv-header": str,
                    "input-packets-with-bad-tlv-type": str,
                    "input-packets-with-bad-type": str,
                    "input-packets-with-discard-type": str,
                    "input-packets-with-too-many-tlvs": str,
                    "input-packets-with-ttp-tlv-p2mp-nbr-nhid-type": str,
                    "input-packets-with-unknown-p2mp-nbr-nhid": str,
                    "input-packets-with-vxlan-bfd-pkts": str,
                    "ipv4-l3-packets-received": str,
                    "ipv4-to-mpls-l3-packets-received": str,
                    "ipv6-l3-packets-received": str,
                    "l2-packets-received": str,
                    "l3-packets-dropped": str,
                    "l3-packets-sent-could-not-get-buffer": str,
                    "mpls-l3-packets-received": str,
                    "mpls-to-ipv4-l3-packets-received": str,
                    "null-l3-packets-received": str,
                    "openflow-packets-received": str,
                    "packets-received-from-unknown-ifl": str,
                    "packets-received-while-unconnected": str,
                    "packets-sent-could-not-find-neighbor": str,
                    "packets-sent-could-not-get-buffer": str,
                    "packets-sent-when-host_unreachable": str,
                    "packets-sent-when-transmit-disabled": str,
                    "packets-sent-while-interface-down": str,
                    "packets-sent-while-unconnected": str,
                    "packets-sent-with-bad-af": str,
                    "packets-sent-with-bad-ifl": str,
                    "tnp-l3-packets-received": str,
                    "ttp-packets-sent": str,
                    "unknown-l3-packets-received": str,
                    "vpls-l3-packets-received": str
                },
                "tudp": {
                    "broadcast-or-multicast-datagrams-dropped-due-to-no-socket": str,
                    "datagrams-dropped-due-to-full-socket-buffers": str,
                    "datagrams-dropped-due-to-no-socket": str,
                    "datagrams-output": str,
                    "datagrams-with-bad-checksum": str,
                    "datagrams-with-bad-data-length-field": str,
                    "datagrams-with-incomplete-header": str,
                    "delivered": str
                },
                "udp": {
                    "datagrams-delivered": str,
                    "datagrams-not-for-hashed-pcb": str,
                    "datagrams-with-bad-datalength-field": str
                }
            }
        ]
    }

class ShowSystemStatistics(ShowSystemStatisticsSchema):
    """ Parser for:
            * show system statistics
    """
    cli_command = 'show system statistics'

    def cli(self, output=None):
        if not output:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        print()
        p1 = re.compile(r'^(?P<state>\S+):$')

        p2 = re.compile(r'^(?P<number_value>\d+) +(?P<key>[\D\s]+)$')

        p3 = re.compile(r'^(?P<number_value_one>\d+) +(?P<key>[\D\s]+)\([(\D+)\s]*(?P<number_value_two>\d+)[(\D+)\s]*\)$')

        p4 = re.compile(r'^(?P<histogram_type>\S+) +Histogram$')

        ret_dict = {}
        self.state = None

        count = 0

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                self.state = group['state']
                continue

            if self.state == 'Tcp':
                continue
                m = p2.match(line)
                if m:
                    group = m.groupdict()
                    key = group['key']
                    key = key.strip()
                    key = key.replace(" ", "_")
                    value = group['number_value']
                    entry = ret_dict.setdefault("statistics", {}).setdefault("tcp", {})
                    if key == "packets_sent":
                        entry['packets-sent'] = value
                    elif key == "resends_initiated_by_MTU_discovery":
                        entry['sent-resends-by-mtu-discovery'] = value
                    elif key == "URG_only_packets":
                        entry['sent-urg-only-packets'] = value
                    elif key == "window_probe_packets":
                        entry['sent-window-probe-packets'] = value
                    elif key == "window_update_packets":
                        entry['sent-window-update-packets'] = value
                    elif key == "control_packets":
                        entry['sent-control-packets'] = value
                    elif key == "packets_received":
                        entry['packets-received'] = value
                    elif key == "duplicate_acks":
                        entry['received-duplicate-acks'] = value
                    elif key == "acks_for_unsent_data":
                        entry['received-acks-for-unsent-data'] = value
                    elif key == "old_duplicate_packets":
                        entry['received-old-duplicate-packets'] = value
                    elif key == "window_probes":
                        entry['received-window-probes'] = value
                    elif key == "window_update_packets":
                        entry['received-window-update-packets'] = value
                    elif key == "packets_received_after_close":
                        entry['packets-received-after-close'] = value
                    elif key == "discarded_for_bad_checksums":
                        entry['received-discarded-for-bad-checksum'] = value
                    elif key == "discarded_for_bad_header_offset_fields":
                        entry['received-discarded-for-bad-header-offset'] = value
                    elif key == "discarded_because_packet_too_short":
                        entry['received-discarded-because-packet-too-short'] = value
                    elif key == "connection_requests":
                        entry['connection-requests'] = value
                    elif key == "connection_accepts":
                        entry['connection-accepts'] = value
                    elif key == "bad_connection_attempts":
                        entry['bad-connection-attempts'] = value
                    elif key == "listen_queue_overflows":
                        entry['listen-queue-overflows'] = value
                    elif key == "connections_established_(including_accepts)":
                        entry['connections-established'] = value
                    elif key == "connections_updated_cached_RTT_on_close":
                        entry['connections-updated-rtt-on-close'] = value
                    elif key == "connections_updated_cached_RTT_variance_on_close":
                        entry['connections-updated-variance-on-close'] = value
                    elif key == "connections_updated_cached_ssthresh_on_close":
                        entry['connections-updated-ssthresh-on-close'] = value
                    elif key == "embryonic_connections_dropped":
                        entry['embryonic-connections-dropped'] = value
                    elif key == "retransmit_timeouts":
                        entry['retransmit-timeouts'] = value
                    elif key == "connections_dropped_by_retransmit_timeout":
                        entry['connections-dropped-by-retransmit-timeout'] = value
                    elif key == "persist_timeouts":
                        entry['persist-timeouts'] = value
                    elif key == "connections_dropped_by_persist_timeout":
                        entry['connections-dropped-by-persist-timeout'] = value
                    elif key == "keepalive_timeouts":
                        entry['keepalive-timeouts'] = value
                    elif key == "keepalive_probes_sent":
                        entry['keepalive-probes-sent'] = value
                    elif key == "connections_dropped_by_keepalive":
                        entry['keepalive-connections-dropped'] = value
                    elif key == "correct_ACK_header_predictions":
                        entry['ack-header-predictions'] = value
                    elif key == "correct_data_packet_header_predictions":
                        entry['data-packet-header-predictions'] = value
                    elif key == "syncache_entries_added":
                        entry['syncache-entries-added'] = value
                    elif key == "retransmitted":
                        entry['retransmitted'] = value
                    elif key == "dupsyn":
                        entry['dupsyn'] = value
                    elif key == "dropped":
                        entry['dropped'] = value
                    elif key == "completed":
                        entry['completed'] = value
                    elif key == "bucket_overflow":
                        entry['bucket-overflow'] = value
                    elif key == "cache_overflow":
                        entry['cache-overflow'] = value
                    elif key == "reset":
                        entry['reset'] = value
                    elif key == "stale":
                        entry['stale'] = value
                    elif key == "aborted":
                        entry['aborted'] = value
                    elif key == "badack":
                        entry['badack'] = value
                    elif key == "unreach":
                        entry['unreach'] = value
                    elif key == "zone_failures":
                        entry['zone-failures'] = value
                    elif key == "cookies_sent":
                        entry['cookies-sent'] = value
                    elif key == "cookies_received":
                        entry['cookies-received'] = value
                    elif key == "SACK_recovery_episodes":
                        entry['sack-recovery-episodes'] = value
                    elif key == "segment_retransmits_in_SACK_recovery_episodes":
                        entry['segment-retransmits'] = value
                    elif key == "byte_retransmits_in_SACK_recovery_episodes":
                        entry['byte-retransmits'] = value
                    elif key == "SACK_options_(SACK_blocks)_received":
                        entry['sack-options-received'] = value
                    elif key == "SACK_options_(SACK_blocks)_sent":
                        entry['sack-opitions-sent'] = value
                    elif key == "SACK_scoreboard_overflow":
                        entry['sack-scoreboard-overflow'] = value
                    elif key == "ACKs_sent_in_response_to_in-window_but_not_exact_RSTs":
                        entry['acks-sent-in-response-but-not-exact-rsts'] = value
                    elif key == "ACKs_sent_in_response_to_in-window_SYNs_on_established_connections":
                        entry['acks-sent-in-response-to-syns-on-established-connections'] = value
                    elif key == "rcv_packets_dropped_by_TCP_due_to_bad_address":
                        entry['rcv-packets-dropped-due-to-bad-address'] = value
                    elif key == "out-of-sequence_segment_drops_due_to_insufficient_memory":
                        entry['out-of-sequence-segment-drops'] = value
                    elif key == "RST_packets":
                        entry['rst-packets'] = value
                    elif key == "ICMP_packets_ignored_by_TCP":
                        entry['icmp-packets-ignored'] = value
                    elif key == "send_packets_dropped_by_TCP_due_to_auth_errors":
                        entry['send-packets-dropped'] = value
                    elif key == "rcv_packets_dropped_by_TCP_due_to_auth_errors":
                        entry['rcv-packets-dropped'] = value
                    elif key == "outgoing_segments_dropped_due_to_policing":
                        entry['outgoing-segments-dropped'] = value

                    continue

                m = p3.match(line)
                if m:
                    group = m.groupdict()
                    key = group['key']
                    key = key.strip()
                    key = key.replace(" ", "_")
                    value_one = group['number_value_one']
                    value_two = group['number_value_two']
                    entry = ret_dict.setdefault("statistics", {}).setdefault("tcp", {})
                    if key == "data_packets":
                        entry['sent-data-packets'] = value_one
                        entry['data-packets-bytes'] = value_two
                    elif key == "data_packets_retransmitted":
                        entry['sent-data-packets-retransmitted'] = value_one
                        entry['retransmitted-bytes'] = value_two
                    elif key == "ack_only_packets":
                        entry['sent-ack-only-packets'] = value_one
                        entry['sent-packets-delayed'] = value_two
                    elif key == "acks":
                        entry['received-acks'] = value_one
                        entry['acks-bytes'] = value_two
                    elif key == "packets_received_in-sequence":
                        entry['packets-received-in-sequence'] = value_one
                        entry['in-sequence-bytes'] = value_two
                    elif key == "completely_duplicate_packets":
                        entry['received-completely-duplicate-packet'] = value_one
                        entry['duplicate-in-bytes'] = value_two
                    elif key == "packets_with_some_duplicate_data":
                        entry['received-packets-with-some-dupliacte-data'] = value_one
                        entry['some-duplicate-in-bytes'] = value_two
                    elif key == "out-of-order_packets":
                        entry['received-out-of-order-packets'] = value_one
                        entry['out-of-order-in-bytes'] = value_two
                    elif key == "packets_of_data_after_window":
                        entry['received-packets-of-data-after-window'] = value_one
                        entry['bytes'] = value_two
                    elif key == "connections_closed":
                        entry['connections-closed'] = value_one
                        entry['drops'] = value_two
                    elif key == "segments_updated_rtt":
                        entry['segments-updated-rtt'] = value_one
                        entry['attempts'] = value_two
                    else:
                        pass
                    continue

            if self.state == 'udp':
                continue
                m = p2.match(line)
                if m:
                    group = m.groupdict()
                    key = group['key']
                    key = key.strip()
                    key = key.replace(" ", "_")
                    value = group['number_value']
                    entry = ret_dict.setdefault("statistics", {}).setdefault("udp", {})

                    if key == "datagrams_received":
                        entry['datagrams-received'] = value
                    elif key == "with_incomplete_header":
                        entry['datagrams-with-incomplete-header'] = value
                    elif key == "with_bad_data_length_field":
                        entry['datagrams-with-bad-datalength-field'] = value
                    elif key == "with_bad_checksum":
                        entry['datagrams-with-bad-checksum'] = value
                    elif key == "dropped_due_to_no_socket":
                        entry['datagrams-dropped-due-to-no-socket'] = value
                    elif key == "broadcast/multicast_datagrams_dropped_due_to_no_socket":
                        entry['broadcast-or-multicast-datagrams-dropped-due-to-no-socket'] = value
                    elif key == "dropped_due_to_full_socket_buffers":
                        entry['datagrams-dropped-due-to-full-socket-buffers'] = value
                    elif key == "not_for_hashed_pcb":
                        entry['datagrams-not-for-hashed-pcb'] = value
                    elif key == "delivered":
                        entry['datagrams-delivered'] = value
                    elif key == "datagrams_output":
                        entry['datagrams-output'] = value

            if self.state == 'ip':
                continue
                m = p2.match(line)
                if m:
                    group = m.groupdict()
                    key = group['key']
                    key = key.strip()
                    key = key.replace(" ", "_")
                    value = group['number_value']
                    entry = ret_dict.setdefault("statistics", {}).setdefault("ip", {})

                    if key == "total_packets_received":
                        entry['packets-received'] = value
                    elif key == "bad_header_checksums":
                        entry['bad-header-checksums'] = value
                    elif key == "with_size_smaller_than_minimum":
                        entry['packets-with-size-smaller-than-minimum'] = value
                    elif key == "with_data_size_<_data_length":
                        entry['packets-with-data-size-less-than-datalength'] = value
                    elif key == "with_header_length_<_data_size":
                        entry['packets-with-header-length-less-than-data-size'] = value
                    elif key == "with_data_length_<_header_length":
                        entry['packets-with-data-length-less-than-headerlength'] = value
                    elif key == "with_incorrect_version_number":
                        entry['packets-with-incorrect-version-number'] = value
                    elif key == "packets_destined_to_dead_next_hop":
                        entry['packets-destined-to-dead-next-hop'] = value
                    elif key == "fragments_received":
                        entry['fragments-received'] = value
                    elif key == "fragments_dropped_(dup_or_out_of_space)":
                        entry['fragments-dropped-due-to-outofspace-or-dup'] = value
                    elif key == "fragment_sessions_dropped_(queue_overflow)":
                        entry['fragments-dropped-due-to-queueoverflow'] = value
                    elif key == "fragments_dropped_after_timeout":
                        entry['fragments-dropped-after-timeout'] = value
                    elif key == "packets_reassembled_ok":
                        entry['packets-reassembled-ok'] = value
                    elif key == "packets_for_this_host":
                        entry['packets-for-this-host'] = value
                    elif key == "packets_for_unknown/unsupported_protocol":
                        entry['packets-for-unknown-or-unsupported-protocol'] = value
                    elif key == "packets_forwarded":
                        entry['packets-forwarded'] = value
                    elif key == "packets_not_forwardable":
                        entry['packets-not-forwardable'] = value
                    elif key == "redirects_sent":
                        entry['redirects-sent'] = value
                    elif key == "packets_sent_from_this_host":
                        entry['packets-sent-from-this-host'] = value
                    elif key == "packets_sent_with_fabricated_ip_header":
                        entry['packets-sent-with-fabricated-ip-header'] = value
                    elif key == "output_packets_dropped_due_to_no_bufs":
                        entry['output-packets-dropped-due-to-no-bufs'] = value
                    elif key == "output_packets_discarded_due_to_no_route":
                        entry['output-packets-discarded-due-to-no-route'] = value
                    elif key == "output_datagrams_fragmented":
                        entry['output-datagrams-fragmented'] = value
                    elif key == "fragments_created":
                        entry['fragments-created'] = value
                    elif key == "datagrams_that_can't_be_fragmented":
                        entry['datagrams-that-can-not-be-fragmented'] = value
                    elif key == "packets_with_bad_options":
                        entry['packets-with-bad-options'] = value
                    elif key == "packets_with_options_handled_without_error":
                        entry['packets-with-options-handled-without-error'] = value
                    elif key == "strict_source_and_record_route_options":
                        entry['strict-source-and-record-route-options'] = value
                    elif key == "loose_source_and_record_route_options":
                        entry['loose-source-and-record-route-options'] = value
                    elif key == "record_route_options":
                        entry['record-route-options'] = value
                    elif key == "timestamp_options":
                        entry['timestamp-options'] = value
                    elif key == "timestamp_and_address_options":
                        entry['timestamp-and-address-options'] = value
                    elif key == "timestamp_and_prespecified_address_options":
                        entry['timestamp-and-prespecified-address-options'] = value
                    elif key == "option_packets_dropped_due_to_rate_limit":
                        entry['option-packets-dropped-due-to-rate-limit'] = value
                    elif key == "router_alert_options":
                        entry['router-alert-options'] = value
                    elif key == "multicast_packets_dropped_":
                        entry['multicast-packets-dropped'] = value
                    elif key == "packets_dropped_(src_and_int_don't_match)":
                        entry['packets-dropped'] = value
                    elif key == "transit_re_packets_dropped_on_mgmt_i/f":
                        entry['transit-re-packets-dropped-on-mgmt-interface'] = value
                    elif key == "packets_used_first_nexthop_in_ecmp_unilist":
                        entry['packets-used-first-nexthop-in-ecmp-unilist'] = value
                    elif key == "incoming_ttpoip_packets_received":
                        entry['incoming-ttpoip-packets-received'] = value
                    elif key == "incoming_ttpoip_packets_dropped":
                        entry['incoming-ttpoip-packets-dropped'] = value
                    elif key == "outgoing_TTPoIP_packets_sent":
                        entry['outgoing-ttpoip-packets-sent'] = value
                    elif key == "outgoing_TTPoIP_packets_dropped":
                        entry['outgoing-ttpoip-packets-dropped'] = value
                    elif key == "raw_packets_dropped._no_space_in_socket_recv_buffer":
                        entry['incoming-rawip-packets-dropped-no-socket-buffer'] = value
                    elif key == "packets_consumed_by_virtual-node_processing":
                        entry['incoming-virtual-node-packets-delivered'] = value

            if self.state == 'icmp':
                m = p2.match(line)
                if m:
                    count += 1
                    group = m.groupdict()
                    key = group['key']
                    key = key.strip()
                    key = key.replace(" ", "_")
                    value = group['number_value']
                    entry = ret_dict.setdefault("statistics", {}).setdefault("udp", {})
                    print(count, key, value)

                    if key == "drops_due_to_rate_limit":
                        entry['temp'] = value
                    elif key == "calls_to_icmp_error":
                        entry['temp'] = value
                    elif key == "errors_not_generated_because_old_message_was_icmp":
                        entry['temp'] = value
                    elif key == "echo_reply":
                        entry['temp'] = value
                        pass
                    elif key == "destination_unreachable":
                        entry['temp'] = value
                        pass
                    elif key == "echo":
                        entry['temp'] = value
                        pass
                    elif key == "time_exceeded":
                        entry['temp'] = value
                        pass
                    elif key == "messages_with_bad_code_fields":
                        entry['temp'] = value
                    elif key == "messages_less_than_the_minimum_length":
                        entry['temp'] = value
                    elif key == "messages_with_bad_checksum":
                        entry['temp'] = value
                    elif key == "messages_with_bad_source_address":
                        entry['temp'] = value
                    elif key == "messages_with_bad_length":
                        entry['temp'] = value
                    elif key == "echo_drops_with_broadcast_or_multicast_destinaton_address":
                        entry['temp'] = value
                    elif key == "timestamp_drops_with_broadcast_or_multicast_destination_address":
                        entry['temp'] = value
                    elif key == "message_responses_generated":
                        entry['temp'] = value
                    continue

        ret_dict['test'] = True
        return ret_dict