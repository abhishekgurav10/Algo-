from multiprocessing import Process
import os

def run_flask_app():
    os.system('python app.py')

def run_backend_trading():
    os.system('python Hedges_1.py')

if __name__ == '__main__':
    p1 = Process(target=run_flask_app)
    p2 = Process(target=run_backend_trading)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
