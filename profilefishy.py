import cProfile

from fishyfrens.app import App

cProfile.run('App.get_instance().start()')  # Replace 'main()' with the main function of your Pygame application
