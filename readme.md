So when run QUITCHATROOM it does not quit entirely and is still running something.
Have to find the error in that part.
The output which could have been fatal is:
KeyboardInterrupt: 
Fatal Python error: _enter_buffered_busy: could not acquire lock for <_io.BufferedWriter name='<stdout>'> at interpreter shutdown, possibly due to daemon threads
Python runtime state: finalizing (tstate=0x0000000103ceeb10)

Current thread 0x00000001fc086080 (most recent call first):
  <no Python frame>
zsh: abort      python3 client.py
jayshah@Jays-MacBook-Air ChatRoom % python3 client.py
Enter your name: ^CTraceback (most recent call last):
  File "/Users/jayshah/Documents/Jay/ChatRoom/client.py", line 4, in <module>
    nickname = input("Enter your name: ")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt


will have to find what is to be done here.