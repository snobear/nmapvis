"""
NmapVis backend lib for nmap scan result parsing and DB CRUD operations
"""
import xml.etree.ElementTree as ET
import sqlite3
from backend.log import setup_logging

log = setup_logging(level='debug', log_to_terminal=True)

def process_file(dbname, filename, filepath, overwrite):
    """entry point: connect to DB and process a given file"""
    conn, cur = dbconnect(dbname)

    parse_xml(conn, cur, filename, filepath, overwrite)

def dbconnect(dbname, dfactory=False):
    try:
        conn = sqlite3.connect(dbname)
        if dfactory:
            conn.row_factory = dict_factory
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()
    except Exception as e:
        log.error("can't connect to database %s. %s" % (dbname, e))
        raise

    return conn, cur

def scan_exists(dbname, filename):
    """Return True if a scan has already been imported"""
    conn, cur = dbconnect(dbname)
    return True if get_scan_id(cur, filename) != None else False

def dict_factory(cursor, row):
    """Used for returing query data as a dict with column names"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_results(dbname):
    """Return port scan results and associated hosts"""
    conn, cur = dbconnect(dbname, dfactory=True)
    cur.execute("""
       select * from scan_results
         inner join scanned_hosts on scan_results.hostscan_id = scanned_hosts.hostscan_id
         inner join scans on scanned_hosts.scan_id = scans.scan_id
    """)
    return cur.fetchall()

def parse_xml(conn, cur, filename, filepath, overwrite):
    """parse nmap xml and ingest into DB"""
    tree = ET.parse(filepath)
    root = tree.getroot()

    runstats = root.find('runstats')
    final_stats = runstats.find('finished').attrib

    # gather info about the scan
    scan_meta = root.attrib
    scan_meta['filename'] = filename
    scan_meta['end'] = final_stats['time']

    scan_id = insert_scan_meta(conn, cur, scan_meta, overwrite)

    # gather info about scanned hosts
    hostslist = []
    scan_results_list = []

    host_child = root.findall('host')

    if not host_child:
        log.info("no hosts found in this scan.")
        return 'no_hosts'

    for host in host_child:
        host_address = host.find('address')
        hostname_data = host.find('hostnames').find('hostname')
        host_status_data = host.find('status')

        hostname = None
        if hasattr(hostname_data, 'attrib'):
            hostname = hostname_data.attrib['name']

        host_state = None
        if hasattr(host_status_data, 'attrib'):
            host_state = host_status_data.attrib['state']

        scanned_host = (
            scan_id,
            host_address.attrib['addrtype'] or None,
            host_address.attrib['addr'] or None,
            hostname,
            host_state,
            host.attrib['starttime'] or None,
            host.attrib['endtime'] or None
        )
        scanned_host_id = insert_scanned_host(conn, cur, scanned_host)

        # gather individual port scan results for this host
        ports = host.find('ports')
        for port in ports:
            if hasattr(port, 'attrib'):
                state = port.find('state')
                service = port.find('service')
                if hasattr(state, 'attrib') and hasattr(service, 'attrib') and port.attrib['portid']:
                    port_scan = (
                        scanned_host_id,
                        port.attrib['portid'],
                        port.attrib['protocol'] or None,
                        state.attrib['state'] or None,
                        service.attrib['name'] or None,
                        state.attrib['reason'] or None
                    )
                    scan_results_list += [port_scan]

    insert_scan_results(conn, cur, scan_results_list)

    # close db connection
    conn.close()

def get_scan_id(cur, filename):
    """
    Returns id of a scan if scan with same filename already exists
    """
    try:
        cur.execute("select scan_id from scans where filename=?", (filename,))
        result = cur.fetchone()

        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        log.error("exception when attempting to look up scan id for filename %s: %s" % (filename,e))
        raise

def delete_scan(conn, cur, scan_id):
    """Delete scan by id. Cascade will delete related scan records per schema."""
    try:
        log.debug("Deleting scan_id=%d" % scan_id)
        cur.execute("delete from scans where scan_id = ?", (scan_id,))
        conn.commit()
    except Exception as e:
        log.error("exception when attempting to delete scan %d: %s" % (scan_id, e))
        raise

def insert_scan_meta(conn, cur, meta, overwrite=False):
    """insert info about a single scan"""
    try:
        log.debug("inserting scan meta: %s" % meta)
        scan_id = get_scan_id(cur, meta['filename'])

        if scan_id and (overwrite == False):
            log.debug("scan exists for file %s, overwrite not selected. No changes made." % meta['filename'])
            return 'exists'

        if scan_id:
            log.debug("scan exists for file %s (scan_id=%d) , overwrite selected" % (meta['filename'], scan_id))
            delete_scan(conn, cur, scan_id)

        # insert
        cur.execute("""
            insert into scans(filename, args, nmap_version, start_dt, end_dt) values (?, ?, ? ,?, ?)
            """,
            (meta['filename'], meta['args'], meta['version'], meta['start'], meta['end'])
        )
        conn.commit()
    except Exception as e:
        log.error("failed to insert metadata about scan: %s" % e)
        raise

    return cur.lastrowid

def insert_scanned_host(conn, cur, hosttuple):
    """insert data about a single host that was scanned"""
    try:
        log.debug("inserting scanned host info: %s" % (hosttuple,))
        cur.execute("""
            insert into scanned_hosts(scan_id,addrtype,addr,hostname,host_state,start_dt,end_dt)
            VALUES (?,?,?,?,?,?,?)
            """, hosttuple)
        conn.commit()
    except Exception as e:
        log.error("failed to insert info about scanned host: %s" % e)
        raise

    return cur.lastrowid

def insert_scan_results(conn, cur, resultlist):
    """bulk insert a list of port scan result tuples"""
    try:
        log.debug("inserting %d scan results" % len(resultlist))
        cur.executemany("""
            insert into scan_results(hostscan_id,port,protocol,state,service_name,reason)
            VALUES (?,?,?,?,?,?)
            """, resultlist)
        conn.commit()
    except Exception as e:
        log.error("bulk insert_scan_results failed: %s" % e)
        raise
