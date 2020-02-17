DROP TABLE IF EXISTS scans;

CREATE TABLE scans (
  scan_id INTEGER PRIMARY KEY,
  filename NVARCHAR(300) UNIQUE NOT NULL,
	args NVARCHAR(300) NOT NULL,
  nmap_version NVARCHAR(50) NULL,
  start_dt INTEGER,
  end_dt INTEGER
);

DROP TABLE IF EXISTS scanned_hosts;

CREATE TABLE scanned_hosts (
  hostscan_id INTEGER PRIMARY KEY,
  scan_id INTEGER NOT NULL,
  addrtype NVARCHAR(10) NULL,
  addr NVARCHAR(50) NULL,
  hostname NVARCHAR(300) NULL,
  state NVARCHAR(100) NULL,
  start_dt INTEGER,
  end_dt INTEGER,
  FOREIGN KEY(scan_id) REFERENCES scans(scan_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS scan_results;

CREATE TABLE scan_results (
  scan_result_id INTEGER PRIMARY KEY,
  hostscan_id INTEGER NOT NULL,
  port INTEGER,
  protocol NVARCHAR(10) NULL,
  state NVARCHAR(50) NULL,
  service_name NVARCHAR(100) NULL,
  reason NVARCHAR(100) NULL,
  FOREIGN KEY (hostscan_id)
   REFERENCES scanned_hosts (hostscan_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);
