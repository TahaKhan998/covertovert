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

        """
        --- We selected the covert channel:
            Covert Storage Channel that exploits Packet Bursting using DNS [Code: CSC-PB-DNS]

        --- This means that the encoding of the data is based on the number of packets sent in a "burst."
            Specifically:
            - Sending 2 packets in a burst encodes a binary `1`.
            - Sending 3 packets in a burst encodes a binary `0`.
        
        --- Now, we will explain the sending code here:

        - Firstly, we suppress a syntax warning caused by the base class's send function to make the output cleaner.

        - Then, we generate a random binary message to send using a helper function from the base class:
            `generate_random_binary_message_with_logging()`. This message is also logged in a file for reference.

        - For each bit in the message:
            - If the bit is `1`, we send a burst of 2 packets.
            - If the bit is `0`, we send a burst of 3 packets.
        
        - After each burst, we introduce a delay (`burst_time`) to separate the bursts. This is crucial to ensure
          the receiver can distinguish between different bursts and count the packets accurately.

        - Once all bits are sent, we send an additional packet to indicate the end of the transmission.
        
        - Originally, we also calculated the total transmission time and covert channel capacity (bits/second),
          but these lines are currently commented out.

        """

        warnings.filterwarnings("ignore", category=SyntaxWarning)

        binary_message =  self.generate_random_binary_message_with_logging(log_file_name)

        # start_time = time.time()


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


        # end_time = time.time()

        # total_time = end_time - start_time
        # capacity = 128 / total_time  
        # print(f"Covert Channel Capacity: {capacity:.2f} bits/second")
        # print(f"{total_time}")

        
    def receive(self, burst_time, log_file_name):
        """
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """

        """
        --- We selected the covert channel:
            Covert Storage Channel that exploits Packet Bursting using DNS [Code: CSC-PB-DNS]

        --- In the receiving function, we will explain how the decoding process works:

        - The receiver listens for packets on UDP port 53 (the DNS communication port).
        
        - For each received packet:
            - We calculate the time difference between the current packet and the previous one.
            - We count how many packets were received in the burst before the time gap exceeds the burst time.

        - Based on the packet count:
            - If 2 packets were received in the burst, it represents a binary `1`.
            - If 3 packets were received in the burst, it represents a binary `0`.

        - These decoded bits are appended to a binary message string. Once we have 8 bits (1 byte), they are
          converted into a character using the base class's helper function:
          `convert_eight_bits_to_character()`.

        - If the character `.` is decoded, it indicates the end of the message, and we stop sniffing further packets.

        - Finally, the decoded message is logged using `log_message()`.

        --- Now, we will explain the key sections of the code:

        1. **Initialization:**
            - `binary_message`: A string to store the binary bits decoded from packet bursts.
            - `decoded_message`: A string to store the final decoded message as characters.
            - `packets_received`: A counter to track how many packets are received in a burst.
            - `last_time`: Stores the timestamp of the last packet for calculating time differences.
            - `message_ended`: A flag to indicate when the message ends.

        2. **Packet Handling Logic:**
            - Each incoming packet triggers the `receive_packet()` function:
                - The time difference between packets is calculated.
                - If the time gap exceeds the `burst_time`, the burst ends, and the packet count is used to
                  decode the bit (`1` or `0`).

        3. **Stop Condition:**
            - The `end()` function returns `True` when the message ends (indicated by `.`), stopping the sniffing loop.

        4. **Logging:**
            - The decoded message is logged at the end of the function for reference.

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





