from threading import Timer, Event


def every_so_often():
    if not done.is_set():
        print('Do the thing you want to every so often')
        Timer(1.0, every_so_often).start()


done = Event()
every_so_often()
# done.set()
