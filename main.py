import pandas as pd
import re #파이썬에서 정규표현식으로 문자열을 검색 및 조작하는 라이브러리
from collections import Counter #요소 빈도계산시 사용되는 라이브러리
from daily_chat_graph import DailyChatGraph



path = input('채팅 csv 파일의 절대주소를 붙여넣기 하세요(윈도우 기준 파일 클릭후 ctrl+shift+c): ')
chat = pd.read_csv(path)
match = re.search(r'KakaoTalk_Chat_(.*?)_', path)
if match:
    name = match.group(1)
    print('%s \b님과의 채팅 내용을 분석합니다\n.\n'% name)
else:
    print('올바른 파일이 아닙니다')

print('개요')

total_chat_count = chat['Message'].count()
print('총 채팅 수: %d개'% total_chat_count)


user_message_counts = chat.groupby('User')['Message'].count()
sorted_user_message_counts = user_message_counts.sort_values(ascending=False) #내림차순 정렬, 시리즈형식
for i, (user, count) in enumerate(sorted_user_message_counts.items(), start=1): #열거형, 색인값도 같이 반환
    print(f"{i}: {user}: {count}개")

previous_user = None
user_message_counts = Counter()
print("\n끊어치기를 반영한 User별 채팅량")
for _, row in chat.iterrows():
    current_user = row['User']
    if current_user != previous_user:
        user_message_counts[current_user] += 1
    previous_user = current_user

sorted_user_message_counts = sorted(user_message_counts.items(), key=lambda x: x[1], reverse=True)
for i, (user, count) in enumerate(sorted_user_message_counts, start=1):
    print(f"{i}: {user}: {count}개")



chat['Date'] = chat['Date'].str.split(' ').str[0]
daily_chat_counts = chat.groupby('Date')['Message'].count()
max_chat_dates = daily_chat_counts.nlargest(5)
min_chat_dates = daily_chat_counts.nsmallest(5)
print("가장 많은 채팅량이 있었던 날짜 TOP 5:")
for i, (date, count) in enumerate(max_chat_dates.items(), start=1):
    print(f"{i}위: {date} ({count}개)")
print("\n가장 적은 채팅량이 있었던 날짜 TOP 5:")
for i, (date, count) in enumerate(min_chat_dates.items(), start=1):
    print(f"{i}위: {date} ({count}개)")

all_messages = ' '.join(chat['Message'].dropna())
word_counts = Counter(all_messages.split())
most_common_word, most_common_count = word_counts.most_common(1)[0]
print(f"전체 채팅에서 가장 많이 사용된 단어: '{most_common_word}' ({most_common_count}번 사용됨)")

if most_common_word == '사진':
    second_most_common_word, second_most_common_count = word_counts.most_common(2)[1]
    print(f"'사진'을 제외한 전체 채팅에서 두 번째로 많이 사용된 단어: '{second_most_common_word}' ({second_most_common_count}번 사용됨)")


user_messages = chat.groupby('User')['Message'].apply(lambda x: ' '.join(x.dropna()))
user_word_counts = user_messages.apply(lambda x: Counter(x.split()))
for user, word_counts in user_word_counts.items():
    sorted_word_counts = word_counts.most_common(5)
    print(f"{user}님이 가장 많이 사용한 단어 TOP 5:")
    for i, (word, count) in enumerate(sorted_word_counts, start=1):
        print(f"{i}: '{word}' ({count}번 사용됨)")


a = chat['Date'].iloc[0]
b= chat['Date'].iloc[-1]
print(f'시작날짜: {a}\n마지막날짜: {b}')
graph_date = DailyChatGraph(path,a,b)
graph_date.graph_date()


