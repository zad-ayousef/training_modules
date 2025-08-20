import xmlrpc.client


class RemoteOdoo:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.sock = None
        self._connect()

    def _connect(self):
        try:

            url_parts = self.url.replace('http://', '').split(':')
            host = url_parts[0]
            port = int(url_parts[1]) if len(url_parts) > 1 else 80

            root = 'http://%s:%d/xmlrpc/' % (host, port)

            self.uid = xmlrpc.client.ServerProxy(root + 'common').login(self.db, self.username, self.password)
            print("Logged in as %s (uid: %d)" % (self.username, self.uid))

            self.sock = xmlrpc.client.ServerProxy(root + 'object')

        except Exception as e:
            print(f"Connection failed: {e}")
            raise

    def search_read(self, model, domain, fields):
        try:
            return self.sock.execute(self.db, self.uid, self.password, model, 'search_read', domain, {'fields': fields})
        except Exception as e:
            print(f"Search_read failed: {e}")
            return []

    def create(self, model, vals):
        try:

            result = self.sock.execute(self.db, self.uid, self.password, model, 'create', vals)
            print(f"Created {model} with ID: {result}")
            return result
        except Exception as e:

            print(f"First attempt failed: {e}")
            try:
                self._connect()  # Reconnect
                result = self.sock.execute(self.db, self.uid, self.password, model, 'create', vals)
                print(f"Created {model} with ID: {result} (after reconnect)")
                return result
            except Exception as e2:
                print(f"Create failed for {model}: {e2}")
                return False

    def write(self, model, ids, vals):
        try:
            return self.sock.execute(self.db, self.uid, self.password, model, 'write', ids, vals)
        except Exception as e:
            print(f"Write failed: {e}")
            return False
