FROM althack/ros2:humble-cuda-gazebo

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /app

WORKDIR /app

RUN apt install -y git

RUN git clone https://github.com/PX4/PX4-Autopilot.git --recursive

RUN bash /app/PX4-Autopilot/Tools/setup/ubuntu.sh

WORKDIR /app/PX4-Autopilot

RUN make px4_sitl

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]