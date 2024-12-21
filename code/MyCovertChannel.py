from CovertChannelBase import CovertChannelBase
from scapy.all import IP, UDP, DNS, sniff
import warnings
import time

class MyCovertChannel(CovertChannelBase):
    """
    - You are not allowed to change the file name and class name.
    - You can edit the class in any way you want (e.g. adding helper functions); however, there must be a "send" and a "receive" function, the covert channel will be triggered by calling these functions.
    """
    def __init__(self):
        """
        - You can edit __init__.
        """
        
    def send(self, log_file_name, receiver_ip, burst_time):
        """
        - In this function, you expected to create a random message (using function/s in CovertChannelBase), and send it to the receiver container. Entire sending operations should be handled in this function.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """

        warnings.filterwarnings("ignore", category=SyntaxWarning)

        binary_message =  self.generate_random_binary_message_with_logging(log_file_name)


        for curr_bit in binary_message:
            if (curr_bit == "1"):
                packets = 2
            else:
                packets = 3

            for i in range(packets):
                packet = IP(dst = receiver_ip)/UDP()/DNS()
                super().send(packet)
        
            
            time.sleep(burst_time)

        time.sleep(burst_time)
        packet = IP(dst = receiver_ip)/UDP()/DNS()
        super().send(packet)
        
    def receive(self, burst_time, log_file_name):
        """
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        binary_message = ""
        decoded_message = ""
        packets_received = 0
        last_time = time.time()
        message_ended = False

        def receive_packet(packet):

            nonlocal binary_message, packets_received, last_time, decoded_message, message_ended

        
            curr_time = time.time()
            time_difference = curr_time - last_time

            packets_received += 1
            last_time = curr_time

          

            if (time_difference > burst_time):
                
                if (packets_received == 2):
                    binary_message += "1"
                    

                elif (packets_received == 3):
                    binary_message += "0"
                
                
                packets_received = 0

                if (len(binary_message) == 8):
                    decoded_message += self.convert_eight_bits_to_character(binary_message)
                    binary_message = ""
                    print("char =", decoded_message[-1])

                    if (decoded_message[-1] == '.'):
                        message_ended = True

            

        def end(_):
            return message_ended

        sniff(filter="udp port 53", prn=receive_packet, stop_filter = end)

        self.log_message(decoded_message, log_file_name)


