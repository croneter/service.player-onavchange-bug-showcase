# -*- coding: utf-8 -*-
# Showcase for Kodi 19.x (and probably 18.x) issue/bug, where the JSON method
# for Player.GetProperties does not return any changes for the subtitle stream
# info even though the subtitle was changed during playback

from json import loads, dumps
import xbmc


class MyMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        self.json = JSON()
        super(MyMonitor, self).__init__(*args, **kwargs)

    def onNotification(self, sender, method, data):
        if method == 'Player.OnAVChange':
            data = loads(data)
            streams = self.json.current_streams(data['player']['playerid'])
            xbmc.log("service.player-onavchange-bug-showcase: "
                     "Player.GetProperties: %s" % streams,
                     level=xbmc.LOGDEBUG)


class JSON(object):
    def __init__(self):
        self._id = 1

    def current_streams(self, playerid):
        query = {
            'jsonrpc': '2.0',
            'id': self._id,
            'method': 'Player.GetProperties',
            'params': {'playerid': playerid,
                       'properties': ['currentaudiostream',
                                      'currentsubtitle',
                                      'subtitleenabled']}

        }
        self._id += 1
        return loads(xbmc.executeJSONRPC(dumps(query)))


def main():
    monitor = MyMonitor()
    while not monitor.abortRequested():
        # sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # abort was requested while waiting. we should exit
            break


if __name__ == '__main__':
    main()
