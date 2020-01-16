zodb_conf: str = """<zodb>
    <zeoclient>
    server localhost:8090
    </zeoclient>
</zodb>
"""

zeo_conf: str = """<zeo>
  address localhost:8090
</zeo>"""

storage_conf: str = """<filestorage>
  path data.fs
</filestorage>

<eventlog>
  <logfile>
    path /tmp/zeo.log
    format %(asctime)s %(message)s
  </logfile>
</eventlog>
"""
