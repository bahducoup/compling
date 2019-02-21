if __name__=='__main__':
    days = ['월', '화', '수', '목', '금', '토', '일']
    
    today = input('오늘은 무슨 요일입니까? ').strip()
    num_days = int(input('며칠 후의 요일을 계산할까요? ').strip())
    
    day_idx = (days.index(today) + num_days) % 7
    print('{}일 후는 {}요일입니다.'.format(num_days, days[day_idx]))
    
