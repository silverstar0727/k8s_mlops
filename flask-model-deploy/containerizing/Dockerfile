# tensorflow/tensorflow는 tensorflow의 공식 이미지 중 하나입니다.
# 이를 기반으로 Dockerfile을 작성합니다.
FROM tensorflow/tensorflow

# Docker 이미지 내부에서 RUN, CMD, ENTRYPOINT의 명령이 실행될 디렉토리를 설정 (작업 폴더 설정)
WORKDIR /app

# 현재 디렉터리에 있는 파일들을 이미지 내부 /app 디렉터리에 복사함
COPY . /app

# 각종 파이썬 라이브러리를 설치합니다.
RUN pip install opencv-contrib-python
RUN pip install Flask
RUN pip install pillow
RUN pip install gunicorn

# opencv가 설치되기 위한 종속성을 리눅스에서 설치합니다.
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install libgl1-mesa-glx -y

# pretrained 폴더를 만듭니다.
RUN mkdir pretrained
# 압축된 모델 파일을 /app/pretrained/model.tar.gz로 다운받습니다.
RUN wget -O ./pretrained/model.tar.gz http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz
# 다운받은 압축파일을 해제합니다.
RUN tar -xvf ./pretrained/model.tar.gz -C pretrained
# 모델에 대한 메타데이터를 다운받습니다.
RUN wget -O ./pretrained/model.pbtxt https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/faster_rcnn_resnet50_coco_2018_01_28.pbtxt

# gunicorn을 이용하여 배포합니다.
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app