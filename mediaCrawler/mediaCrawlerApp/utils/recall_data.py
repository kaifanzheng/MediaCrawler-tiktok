# mediaCrawlerApp/utils/send_excel_to_frontend.py
import random
import string
import pandas as pd
import time
import io

def send_excel_to_frontend():
    print("后端发送表格给前端下载")
    time.sleep(10)
    data = {
        "Column1": [''.join(random.choices(string.ascii_letters, k=3)) for _ in range(500)]
    }
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)  # 将指针移到文件的开始位置
    print("发送成功")
    return output

# def send_excel_to_frontend():
#     print("后端发送表格给前端下载")
#     file_path = r"C:\Users\Administrator\Desktop\demo_excel_file.xlsx"
#     generate_random_excel(file_path)
#     return file_path
