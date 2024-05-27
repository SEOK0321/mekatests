import subprocess

try:
    # subprocess를 통해 testserver.py를 호출하여 결과 받아오기
    result1 = subprocess.run(["python", "testsensor1.py"], capture_output=True, text=True)
    result2 = subprocess.run(["python", "testsensor2.py"], capture_output=True, text=True)

    # 결과 출력
    if int(result1.stdout) <= 20 or int(result2.stdout) <= 20:
        print("OK")
    else:
        print("NO")

except subprocess.CalledProcessError as e:
    print("Error running testserver.py:", e)

except KeyboardInterrupt:
    print("Program terminated by user")
