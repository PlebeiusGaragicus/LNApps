class ViewState:
    def __init__(self):
        pass

    def setup(self):
        raise NotImplementedError(f"setup() not implemented in {self.__class__.__name__} class")

    def handle_event(self, event):
        raise NotImplementedError(f"handle_event() not implemented in {self.__class__.__name__} class")

    def update(self):
        raise NotImplementedError(f"update() not implemented in {self.__class__.__name__} class")

    def draw(self):
        raise NotImplementedError(f"draw() not implemented in {self.__class__.__name__} class")



class ViewStateManager:
    def __init__(self):
        self.states = {}
        self.current_state: ViewState = None

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        self.current_state = self.states[name]
        self.states[name].setup()

    def handle_event(self, event):
        self.current_state.handle_event(event)

    def update(self):
        self.current_state.update()

    # def draw(self, screen):
    #     self.current_state.draw(screen)
    def draw(self):
        self.current_state.draw()
