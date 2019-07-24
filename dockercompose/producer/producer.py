from kafka import KafkaConsumer, KafkaProducer
import threading, logging, time
import json
import random

class Producer(threading.Thread):
    def __init__(self):
        self.ama = {"name" : "AMZN", "price" : 1902} 
        self.msft = {"name" : "MSFT", "price" : 107} 
        

        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def generate_data(self):
        data = [self.ama, self.msft]
        for stock in data:
           price = stock['price'] * (1.0 + random.uniform(-0.1, 0.1))
           stock['price'] = price
           print(price)

        result = json.dumps(data)
        print('I have stocks: ' + result)
        return result
       
    def run_test(self):
        while not self.stop_event.is_set():
            self.generate_data()
            time.sleep(5)

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        data = [self.ama, self.msft]

        while not self.stop_event.is_set():
           for stock in data:
             price = stock['price'] * (1.0 + random.uniform(-0.1, 0.1))
             stock['price'] = price
             result = json.dumps(stock)
             print(price)
             producer.send('stock', bytes(result, encoding= 'utf-8'))
           time.sleep(1)

        producer.close()


def main():
    time.sleep(10)
    t = Producer()
    t.run()
        
if __name__ == "__main__":
   main()
