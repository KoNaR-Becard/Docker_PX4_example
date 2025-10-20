FROM althack/ros2:humble-cuda-gazebo-2025-05-01

ENV DEBIAN_FRONTEND noninteractive

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | gpg --dearmor --batch --yes -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add the ROS 2 repository for humble (Ubuntu 22.04 is "Jammy")
RUN echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu jammy main" > /etc/apt/sources.list.d/ros2.list

RUN mkdir /app

WORKDIR /app

RUN apt install -y git

RUN git clone https://github.com/PX4/PX4-Autopilot.git --recursive

RUN bash /app/PX4-Autopilot/Tools/setup/ubuntu.sh

WORKDIR /app/PX4-Autopilot

RUN make px4_sitl

WORKDIR /app

RUN git clone -b v2.4.3 https://github.com/eProsima/Micro-XRCE-DDS-Agent.git

WORKDIR /app/Micro-XRCE-DDS-Agent

RUN mkdir build

WORKDIR /app/Micro-XRCE-DDS-Agent/build

RUN cmake ..

RUN make

RUN make install

RUN ldconfig /usr/local/lib

WORKDIR /app/PX4-Autopilot

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]