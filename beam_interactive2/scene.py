from ._util import Resource


class Scene(Resource):
    """
    Scene is a container for controls in interactive. Groups can be assigned
    to scenes. It emits:

     - A ``delete`` event when the scene is deleted, with the Call from
       "onSceneDelete".

     - An ``update`` event when the scene is updated, with the Call from
       "onSceneUpdate".
    """

    def __init__(self, scene_id, **kwargs):
        super(Scene, self).__init__(scene_id, id_property='sceneID')
        self.assign(**kwargs)
        self._controls = {}
        self._control_kinds = {
            'button': Button,
            'joystick': Joystick,
        }

    @property
    def controls(self):
        """
        :rtype: list of Control
        """
        return self._controls

    async def delete(self, reassign_scene_id='default'):
        """
        Deletes the scene from Interactive. Takes the id of the scene
        to reassign any groups who are on that scene to.
        :param reassign_scene_id:
        :type reassign_scene_id: str
        :rtype: None
        """
        await self._connection.call('deleteScene', {
            'sceneID': self.id,
            'reassignSceneID': reassign_scene_id,
        })

    async def update(self, priority=0):
        """
        Saves all changes updates made to the scene.
        """
        return await self._connection.call(
            'updateScenes',
            {'scenes': [self._capture_changes()], 'priority': priority}
        )

    async def create_controls(self, *controls):
        """
        Can be called with one or more Controls to add them to to the scene.
        :param controls: list of controls to create
        :type controls: Control
        """
        for control in controls:
            self._controls[control.id] = control
            control._attach_scene(self)

        return await self._connection.call('createControls', {
            'sceneID': self.id,
            'controls': controls,
        })

    def set_controls(self, controls):
        """
        Can be called with one or more controls to add them to the scene.
        :param controls: list of controls to create
        """
        for control in controls:
            temp_button = Button(control_id=control['controlID'],
                                                          text=control['text'],
                                                          keycode=control['keyCode'],
                                                          position=control['position'],
                                                          )
            self._controls[temp_button] = temp_button 
            temp_button._attach_scene(self)
        #     self._controls[control.id] = control
        #     control._attach_scene(self)

    def to_json(self):
        props = super().to_json()
        props['controls'] = [c.to_json() for c in self._controls]
        return props

    def _on_deleted(self, call):
        super()._on_deleted(call)
        for control in self._controls:
            control._on_deleted(call)

    def _on_control_delete(self, call):
        for control_id in call.data['controlIDs']:
            if control_id in self._controls:
                self._controls[control_id]._on_deleted(call)
                del self._controls[control_id]

    def _on_control_update_or_create(self, call):
        for update in call.data['controls']:
            if update['controlID'] not in self._controls:
                c = self._control_kinds[update['kind']](update['controlID'])
                c._attach_connection(self._connection)
                self._controls[update['controlID']] = c

            self._controls[update['controlID']]._apply_changes(update, call)


class Control(Resource):
    """
    Control is a structure on which participants in interactive provide input.
    It emits:

     - A ``delete`` event when the control is deleted, with the Call from
       "onControlDelete".

     - An ``update`` event when the control is updated, with the Call from
       "onControlUpdate".

     - An ``input`` event is fired when input is given on the control.
    """

    def __init__(self, control_id, **kwargs):
        super(Control, self).__init__(control_id, id_property='controlID')
        self._scene = None
        self.assign(**kwargs)

    def _attach_scene(self, scene):
        self._scene = scene
        self._attach_connection(scene._connection)

    def _give_input(self, call):
        self.emit(call.data['input']['event'], call)

    async def delete(self):
        """
        Deletes the control
        :return: None
        """
        await self._connection.call('deleteControls', {
            'sceneID': self._scene.id,
            'controlIDs': [self.id],
        })

    async def update(self):
        """
        Saves all changes updates made to the control.
        """
        await self._connection.call('updateControls', {
            'sceneID': self._scene.id,
            'controls': [self._capture_changes()],
        })


class Button(Control):
    def __init__(self, control_id, **kwargs):
        super().__init__(control_id)
        kwargs['kind'] = 'button'
        self.assign(**kwargs)


class Joystick(Control):
    def __init__(self, control_id, **kwargs):
        super().__init__(control_id)
        kwargs['kind'] = 'joystick'
        self.assign(**kwargs)
