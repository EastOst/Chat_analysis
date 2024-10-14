import matplotlib.pyplot as plt
import pandas as pd
import datetime



class DailyChatGraph:
    def __init__(self, path, start_date,finish_date):
        self.chat = pd.read_csv(path)
        self.chat['Date'] = self.chat['Date'].str.split().str[0]
        self.chat['Date'] = pd.to_datetime(self.chat['Date'])
        self.start_date = start_date
        self.finish_date = finish_date
        mask = (self.chat['Date']>=self.start_date) & (self.chat['Date']<=self.finish_date)
        self.filterd_chat = self.chat[mask]

    def setting(self):
        self.date_message_count = self.filterd_chat.groupby('Date')['Message'].count()
    def graph_date(self):
        self.setting()
        plt.figure(figsize=(12, 6))  # 그래프 크기 조정
        plt.bar(self.date_message_count.index, self.date_message_count.values, color='b', alpha=0.7)  # 막대 그래프로 변경
        plt.title('Number of Messages Per Day')  
        plt.xlabel('Date')
        plt.ylabel('Number of Messages')
        plt.grid(axis='y')  
        plt.xticks(rotation=45)  # x 축 라벨 회전
        plt.xlim(datetime.datetime(2024, 10, 9), datetime.datetime(2024, 10, 14))  # 날짜조정
        plt.tight_layout()  # 그래프 간격 조정
        plt.show()







