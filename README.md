물론입니다! 아래는 `yaw_offset_estimator` ROS 2 패키지를 위한 **README.md 예시**입니다.  
이 파일은 GitHub 저장소 최상단에 위치하게 되며, 사용법과 원리, 설치법 등을 한눈에 보여줍니다.

---

```markdown
# 🧭 yaw_offset_estimator

ROS 2 패키지 `yaw_offset_estimator`는 GPS와 IMU 데이터를 이용해 `navsat_transform_node`에 필요한 `yaw_offset` 값을 자동으로 계산하는 유틸리티 노드입니다.  
이 보정값을 통해 SLAM 좌표계(map)와 GPS(ENU) 좌표계 사이의 방향 정렬 문제를 해결할 수 있습니다.

---

## ✅ 주요 기능

- `/imu/data`에서 yaw(방위각)를 추출
- `/gps/fix`에서 두 위치를 받아 이동 방향(GPS heading) 계산
- 자기 편차(magnetic declination) 반영
- 계산된 `yaw_offset`을 로그로 출력하여 `navsat_transform_node`에 적용 가능

---

## 📦 설치

```bash
cd ~/ros2_ws/src
git clone https://github.com/IMSLGGYU/yaw_offset_estimator.git
cd ~/ros2_ws
colcon build --packages-select yaw_offset_estimator
source install/setup.bash
```

---

## ▶️ 실행 방법

로봇이 정지 상태에서, IMU와 GPS가 모두 수신되고 있어야 합니다.

```bash
ros2 run yaw_offset_estimator yaw_offset_estimator
```

옵션으로 자기 편차(degree) 설정 가능:

```bash
ros2 run yaw_offset_estimator yaw_offset_estimator --ros-args -p magnetic_declination_deg:=12.5
```

---

## 📈 출력 예시

```bash
[INFO] IMU Yaw (rad): -1.5708
[INFO] GPS Heading (rad): 0.0000
[INFO] Yaw Offset (rad): 1.5708
[INFO] Yaw Offset (deg): 90.00
```

---

## 🧭 `navsat_transform_node` 설정 예시

```yaml
navsat_transform_node:
  ros__parameters:
    yaw_offset: 1.5708
    magnetic_declination_radians: 0.218  # (optional)
```

---

## 💡 팁

- SLAM 지도는 x축이 동쪽을 바라보도록 정렬되어 있어야 합니다.
- GPS와 IMU는 시간 동기화가 잘 되어 있어야 합니다.
- 로봇이 정지 상태에서 실행해야 정확한 heading 계산이 가능합니다.

---

## 🛠️ TODO (계획 중)

- 자기 편차 자동 계산 기능 (위도/경도 기반)
- yaw_offset 자동 설정 노드 또는 launch 연동
- RViz 시각화 지원

---

## 📜 라이선스

MIT License

---

## 🙋‍♀️ 개발자

**IMSLGGYU**  
📧 gbkmgsc1@gmail.com  
🌐 https://github.com/IMSLGGYU
```

---

이 README를 `yaw_offset_estimator/README.md` 파일로 저장하시면 됩니다.  
필요하시면 이미지, RViz 스크린샷, launch 예시도 추가해드릴게요 😎

업로드하셨으면 GitHub 주소 알려주시면 더 다듬어드릴 수도 있어요!
