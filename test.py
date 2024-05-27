import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import subprocess
import torch # torch 라이브러리 추가

# 모델 로드
model = YOLO("best.pt")

def check_scooter():
    try:
        result = subprocess.run(['python', 'testOKorNO.py'], capture_output=True, text=True, timeout=10)
        output = result.stdout.strip()
        if output == "OK":
            return True
        elif output == "NO":
            return False
        else:
            st.error("testOKorNO.py 결과를 확인할 수 없습니다.")
            return None
    except subprocess.TimeoutExpired:
        st.error("testOKorNO.py 실행이 시간 초과되었습니다.")
        return None
    except Exception as e:
        st.error(f"에러 발생: {e}")
        return None

def main():
    st.title("주차 검사")

    uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # 이미지를 RGB로 변환
        img = np.array(image.convert('RGB'))

        # 사진 표시
        st.image(image, caption="업로드된 사진", use_column_width=True)

        sensor_present = check_scooter()

        if sensor_present is not None:
            # 결과 예측
            results = model.predict(
                img,
                save=False,
                imgsz=640,
                conf=0.2,
                device="cuda" if torch.cuda.is_available() else "cpu",  # GPU 사용 가능 여부 확인
            )

            # 검사 결과 분석
            car_present = False
            scooter_detected = False

            for r in results:
                cls = r.boxes.cls
                cls_dict = r.names

                for cls_number in cls:
                    cls_number_int = int(cls_number.item())
                    cls_name = cls_dict[cls_number_int]

                    if cls_name == "Car":
                        car_present = True
                    elif cls_name == "Scooter":
                        scooter_detected = True

            # 검사 결과 메시지 표시
            if car_present and scooter_detected:
                st.error("주차 불가")
            elif not scooter_detected:
                st.warning("스쿠터가 없습니다")
            elif scooter_detected and not car_present and sensor_present:
                st.success("주차 가능")
            elif scooter_detected and not sensor_present:
                st.error("스쿠터를 붙여주세요")
            else:
                st.error("알 수 없는 오류 발생")

if __name__ == "__main__":
    main()
