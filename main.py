# 파일이름 : 날씨에 따른 사용자 매니저 시스템
# 작 성 자 : 60231805 신성수
### 사용자 입력 부분 ###
name = input("사용자님의 이름을 입력하세요: ")
temp = float(input("현재 기온을 입력하세요(°C): "))

ex_temp = []
for i in range(3):
    temp_input = float(input(f"{i+1}시간 후 예상 기온을 입력하세요(°C): "))
    ex_temp.append(temp_input)

humidity = float(input("현재 습도를 입력하세요(%): "))
wind = float(input("현재 풍속을 입력하세요(Km/h): "))
rain_prob = int(input("강수 확률을 입력하세요(%): "))
dust = int(input("미세먼지 수치를 입력하세요(µg/m³): "))

### 기본 출력부분 시작 ###
print("--------------------------------------------------------------------------------------")
print(f"{name}님, 오늘의 날씨 브리핑 시작하겠습니다!!")
print(f"\n먼저 향후 3시간 동안 최고 기온은 {max(ex_temp)}°C 이고, 평균 온도는 {sum(ex_temp)/len(ex_temp):.1f}°C 입니다.")

### 불쾌지수 및 체감온도 계산 및 출력 부분 ###
real_temp, thi = 0, 0
stress_index = 0

if temp <= 10:
    real_temp = 13.12 + 0.6215*temp - 11.37*(wind**0.16) + 0.3965*temp*(wind**0.16)
elif temp >= 20:
    thi = 0.81*temp + 0.01*humidity*(0.99*temp - 14.3) + 46.3

if real_temp != 0:
    print(f"현재 기온은 {temp}°C이지만, 바람이 불어 실제 체감온도는 {real_temp:.1f}°C입니다.")
    stress_index += 15
elif thi != 0:
    if thi >= 80:
        thi_di = "대부분이 불쾌감을 느끼는 날씨"
        stress_index += 20
    elif thi >= 75:
        thi_di = "절반 이상이 불쾌감을 느끼는 날씨"
        stress_index += 15
    elif thi >= 70:
        thi_di = "일부가 불쾌감을 느끼기 시작하는 날씨"
        stress_index += 5
    else:
        thi_di = "쾌적한 날씨"
    print(f"현재 불쾌지수: {thi:.1f} / {thi_di}입니다.")
else:
    print("야외 활동하기 쾌적한 기온입니다.")

### 준비물 리스트 추가 및 출력 부분 ###
items = []

if rain_prob >= 60:
    items.append("우산")
    stress_index += 20
if dust >= 81:
    items.append("마스크")
    stress_index += 10
if real_temp < 0:
    items.append("핫팩")
    stress_index += 5
if temp >= 28 and rain_prob < 60:
    items.append("휴대용 선풍기")
    stress_index += 10

if items:
    print("오늘의 준비물!:", end = " ")
    count = 0
    for item in items:
        count += 1
        if count == len(items):
            print(item)
        else:
            print(item, end = ", ")
else:
    print("오늘의 준비물은 없습니다. 가방이 가벼워지겠네요!")

print(f"마지막으로 오늘의 외출 피로도(스트레스) 지수는 {stress_index}입니다. 오늘 하루도 행복하세요!")
