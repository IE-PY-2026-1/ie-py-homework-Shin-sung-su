# 파일이름 : 날씨에 따른 사용자 매니저 시스템
# 작 성 자 : 60231805 신성수

# 전역 변수 초기화 #
stress_index = 0
name = ""

# 1. 정보 입력 함수 #
def input_weather_info():
    global name
    name = input("사용자님의 이름을 입력하세요: ")
    temp = float(input("현재 기온을 입력하세요(°C): "))

    ex_temp = []
    for i in range(3):
        t = float(input(f"{i+1}시간 후 예상 기온을 입력하세요(°C): "))
        ex_temp.append(t)

    humidity = float(input("현재 습도를 입력하세요(%): "))
    wind = float(input("현재 풍속을 입력하세요(Km/h): "))
    rain_prob = int(input("강수 확률을 입력하세요(%): "))
    dust = int(input("미세먼지 수치를 입력하세요(µg/m³): "))

    return [temp, ex_temp, humidity, wind, rain_prob, dust]

# 2. 불쾌지수 및 체감온도 계산 함수 #
def check_index(temp, humidity, wind):
    real_temp, thi = 0, 0
    global stress_index

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
    
    return real_temp

# 3. 준비물 추천 함수 #
def suggest_items(rain_prob, dust, real_temp, temp):
    global stress_index
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

# 4. 정보 입력 검사 함수 #
def check_data(data):
    if not data:
        print("먼저 1번 메뉴에서 정보를 입력해주세요!")
        return False
    return True 

# 5. 메인 메뉴 함수
def main_menu():
    weather_data = []
    
    while True:
        print("\n----🌦️ 스마트 날씨 매니저 메뉴 ----")
        print("1. 날씨 정보 입력")
        print("2. 오늘 기온 통계 보기")
        print("3. 불쾌/체감 지수 확인 ")
        print("4. 준비물 및 스트레스 지수 확인")
        print("5. 프로그램 종료")

        choice = input("-> 원하시는 메뉴 번호를 입력하세요: ")
        print("")

        if choice == '1':
            weather_data = input_weather_info()
            print("\n정보가 저장되었습니다.")

        elif choice == '2':
            if check_data(weather_data):
                ex_temp = weather_data[1]
                print(f"향후 3시간 최고 기온: {max(ex_temp)}°C")
                print(f"평균 온도: {sum(ex_temp)/len(ex_temp):.1f}°C")

        elif choice == '3':
            if check_data(weather_data):
                weather_data.append(check_index(weather_data[0], weather_data[2], weather_data[3]))

        elif choice == '4':
            if check_data(weather_data):
                if len(weather_data) < 7:
                    print("\n[안내] 3번 메뉴(지수 확인)먼저 실행하여 체감온도를 계산해 주세요!")
                    continue
                suggest_items(weather_data[4], weather_data[5], weather_data[-1], weather_data[0])
                print(f"현재 {name}님의 외출 피로도 지수는 {stress_index}입니다.")
        
        elif choice == '5':
            print("매니저를 종료합니다. 행복한 하루 되세요!")
            break

        else:
            print("잘못된 입력입니다. 1~5번 사이를 선택해주세요.")

# 프로그램 시작 #
main_menu()