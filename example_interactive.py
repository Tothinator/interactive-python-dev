from beam_interactive2 import State, Scene, Button, keycode, until_event
from helpers import get_access_token
import config_interactive
import asyncio

config = config_interactive

class QuitException(Exception):
        pass

class Example():
        def __init__(self):
                self._interactive = None
                self._access_token = get_access_token()

        def _on_participant_join(self, call):
            print('Hi There')
            # user = call.data['params']['participants']['userID']
      
        async def setup(self):

                try:
                        self._interactive = await State.connect(authorization="Bearer " + self._access_token,
                                                          project_version_id=config.VERSION_ID)
                except Exception as e:
                        print("Error connecting to interactive", e)
                        return

                scenes = await self._interactive.get_scenes()

                # print(scenes)

                self._interactive.set_scenes(scenes)

                for sid in scenes['scenes']:
                    for s in self._interactive._scenes:
                        if s == sid['sceneID']:
                            self._interactive._scenes[s].set_controls(sid['controls'])
                            # print(s)
                            # print(sid['controls'])

                # print(self._interactive._scenes)

                self._interactive.scenes.update()

                self._interactive.pump_async()

                self._interactive.on('onParticipantJoin', lambda call: print('Hi user'))

        async def loop(self):
                await self.setup()

                test = None
                for key in self._interactive.scenes['default']._controls:
                    test = key

                test.on('mousedown', lambda call: print('This is a Test'))

                await self._interactive.set_ready()

                while True:
                    await asyncio.sleep(1)



def run(game):
    loop = asyncio.get_event_loop() 
    try:
        loop.run_until_complete(game.loop())
    except (KeyboardInterrupt, QuitException):
        game._interactive._connection.close()
    finally:
        loop.stop()

if __name__ == '__main__':
	run(Example())