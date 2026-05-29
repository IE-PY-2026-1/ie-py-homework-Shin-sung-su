# 파일이름 : 날씨에 따른 사용자 매니저 시스템
# 작 성 자 : 60231805 신성수

# 전역 변수 초기화 #
stress_index = 0
name = ""

# 1. 정보 입력 함수 #
def input_weather_info():
    global name
    name = input("사용자님의 이름을 입력하세요: ")

    try: 
        temp = float(input("현재 기온을 입력하세요(°C): "))

        ex_temp = []
        days = ["오늘", "내일"]
        times = ["오전", "오후"]

        print("\n[향후 이틀간의 예상 기온을 입력합니다.]")
        for d in days:
            daily_temp = []
            for t in times:
                t_input = float(input(f"{d} {t} 예상 기온을 입력하세요(°C): "))
                daily_temp.append(t_input)
            ex_temp.append(daily_temp)

        humidity = float(input("현재 습도를 입력하세요(%): "))
        wind = float(input("현재 풍속을 입력하세요(Km/h): "))
        rain_prob = int(input("강수 확률을 입력하세요(%): "))
        dust = int(input("미세먼지 수치를 입력하세요(µg/m³): "))

        return [temp, ex_temp, humidity, wind, rain_prob, dust]
    
    except ValueError:
        print("/n [입력 오류] 숫자만 입력 가능합니다. 다시 시도해주세요.")
        return []

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

# 5. 파일 저장 함수 #
def save_report(data):
    ex_temp = data[1]
    days = ["오늘", "내일"]
    times = ["오전", "오후"]

    try:
        with open("weather_report.txt", "w", encoding="utf-8") as f:
            f.write(f"--- {name}님의 스마트 날씨 리포트 ---\n")
            f.write(f"현재 기온: {data[0]}°C / 습도: {data[2]}%\n\n")
            f.write("[예상 기온 상세 현황]\n")

            for i in range(len(ex_temp)):
                f.write(f"- {days[i]}")
                for j in range(len(ex_temp[i])):
                    f.write(f"{times[j]}({ex_temp[i][j]}°C)")
                f.write("\n")

            f.write(f"\n누적 외출 피로도 지수: {stress_index}\n")
            f.write("-" * 45)
        print("\n 'weather_report.txt'로 저장이 완료되었습니다.")
    except Exception as e:
        print(f"파일 저장 실패: {e}")

# 6. 메인 메뉴 함수 #
def main_menu():
    weather_data = []
    
    while True:
        print("\n----🌦️ 스마트 날씨 매니저 메뉴 ----")
        print("1. 날씨 정보 입력")
        print("2. 기온 상세 현황")
        print("3. 불쾌/체감 지수 확인 ")
        print("4. 준비물 및 스트레스 지수 확인")
        print("5. 파일 저장")
        print("6. 프로그램 종료")

        choice = input("-> 원하시는 메뉴 번호를 입력하세요: ")
        print("")

        if choice == '1':
            weather_data = input_weather_info()
            if weather_data:
                print("\n정보가 저장되었습니다.")
    
        elif choice == '2':
            if check_data(weather_data):
                ex_temp = weather_data[1]
                days = ["오늘", "내일"]
                times = ["오전", "오후"]

                print("\n[향후 예상 기온 상세 현황]")
                for i in range(len(ex_temp)):
                    print(f"> {days[i]} 데이터:", end = " ")
                    for j in range(len(ex_temp[i])):
                        print(f"{times[j]} {ex_temp[i][j]}°C", end = " | ")
                    print()

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
            if check_data(weather_data):
                save_report(weather_data)

        elif choice == '6':
            print("매니저를 종료합니다. 행복한 하루 되세요!")
            break

        else:
            print("잘못된 입력입니다. 1~6번 사이를 선택해주세요.")

# 프로그램 시작 #
main_menu()