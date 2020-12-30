import signal

class InputTimeoutError(Exception):
    pass

def interrupted(signum, frame):
    raise InputTimeoutError


signal.signal(signal.SIGALRM, interrupted)
signal.alarm(10)


if __name__ == '__main__':
    content = "This is a post example"
    comment = "This is a comment example"
    print("content:" + content)
    print("comment:" + comment)
    try:
        comment = input("Do you agree to Comment? Input nothing to confirm or input an appropriate sentence:")
    except InputTimeoutError:
        print('\n Agree to comment')

    print("chatbot will comment on this sentence:"+comment)

    signal.alarm(0)  # 读到输入的话重置信号