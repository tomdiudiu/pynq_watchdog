#encoding=utf-8
import random

def GD(N):
    num = 1
    list_total = []
    while num <= N:
        # n = random.randint(1,40)
        n = int(random.normalvariate(4,10))^2
        while(n<1 or n>40):
            n = int(random.normalvariate(4,10))^2
        list_sub = []
        for i in range(n):
            list_sub_sub = []
            # d = random.randint(10,20)
            # h = random.randint(0,23)
            # m = random.randint(0,59)
            # s = random.randint(0,59)
            # io = random.randint(0,1)
            d = int(random.normalvariate(3,5))^2
            while(d<10 or d>20):
                d = int(random.normalvariate(3, 5)) ^ 2

            h = int(random.normalvariate(3, 5)) ^ 2
            while (h < 10 or h > 20):
                h = int(random.normalvariate(3, 5)) ^ 2
            m = int(random.normalvariate(5, 5)) ^ 2
            while (m < 0 or m > 59):
                m = int(random.normalvariate(5, 5)) ^ 2
            s = int(random.normalvariate(5, 5)) ^ 2
            while (s < 0 or s > 59):
                s = int(random.normalvariate(5, 5)) ^ 2
            io = random.randint(0, 1)
            if h<10:
                h_str = '0'+str(h)
            else:
                h_str = str(h)
            if m<10:
                m_str = '0'+str(m)
            else:
                m_str = str(m)
            if s<10:
                s_str = '0'+str(s)
            else:
                s_str = str(s)
            if io == 0:
                io_str = 'in'
            else:
                io_str = 'out'
            datetime = '2019/11/'+str(d)+'/'+h_str+'/'+m_str+'/'+s_str+'/'+s_str
            list_sub_sub.append(datetime)
            list_sub_sub.append(io_str)

            list_sub.append(list_sub_sub)
        list_total.append(list_sub)
        num += 1
    return list_total



