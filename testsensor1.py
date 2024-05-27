import serial

# 시리얼 포트 설정 (아두이노의 포트에 맞게 수정)
# serial_port = '/dev/ttyUSB0'  # 리눅스 예시
serial_port = 'COM3'            # 윈도우 예시

# 시리얼 통신 속도 설정 (아두이노와 동일하게)
baud_rate = 9600

try:
    # 시리얼 포트 연결
    with serial.Serial(serial_port, baud_rate) as ser:

        # 시리얼 포트에서 데이터 한 줄씩 읽기
        line = ser.readline().decode().strip()
        # 쉼표를 기준으로 데이터를 분리하여 거리 값을 추출
        distances = line.split(",")
        if len(distances) == 2:
            distance1 = int(distances[0])
            print(distance1)
        else:
            print("Invalid data received:", line)

except serial.SerialException as e:
    print("Serial connection error:", e)

except KeyboardInterrupt:
    print("Program terminated by user")
