from flask_restful import abort


class Ping:
    pings = {
        1: "Ping 1",
        2: "Ping 2",
        3: "Ping 3"
    }

    def get(self, ping_id=None):
        if ping_id is None:
            return self.pings, 200
        else:
            self.abort_if_ping_doesnt_exist(ping_id)
            return {'id': ping_id, 'response': self.pings[ping_id]}, 200

    def delete(self, ping_id):
        self.abort_if_ping_doesnt_exist(ping_id)
        del self.pings[ping_id]
        return '', 204

    def abort_if_ping_doesnt_exist(self, ping_id):
        if ping_id not in self.pings:
            abort(404, message="Ping {} doesn't exist".format(ping_id))
