Socket Programming: FTP Client
ในการสร้างโปรแกรมด้วยภาษา Python เพื่อพัฒนาเลียนแบบคำสั่ง ftp ในระบบปฏิบัติการ Windows ผู้เรียนได้ทำการพัฒนาคำสั่งโปรแกรม ftp ต่อไปนี้

•โครงสร้างหลักของโปรแกรมสามารถทำงานแบบ Read-Evaluate-Print-Loop (REPL) และรับคำสั่งได้ 
•ascii(2 คะแนน)
•binary(2 คะแนน)
•bye(1 คะแนน)
•cd(2 คะแนน)
•close(1 คะแนน)
•delete(2 คะแนน)
•disconnect(1 คะแนน)
•get(2 คะแนน)
•ls(2 คะแนน)
•open(2 คะแนน)
•put(2 คะแนน)
•pwd(2 คะแนน)
•quit(1 คะแนน)
•rename(2 คะแนน)
•user(2 คะแนน)

ส่วนการทำงานของคำสั่งมีความคล้ายคลึงกับคำสั่ง ftp ใน Windows 11
*หมายเหตุ
    -มีการเรียกใช้ os ในการตรวจสอบชื่อไฟล์ว่ามีอยู่ใน directory หรือไม่ในฟังก์ชัน put
    -เมื่อต้องการรันใหม่ให้ทำการ เรียกคำสั่ง quit ออกก่อน
    -ไฟล์หลักที่ใช้ในการรันโปรแกรมคือ myftp.py
โดยมีส่วนที่ไม่เหมือนกับต้นฉบับ ได้แก่
- คำสั่งนอกเหนือจากคำสั่งด้านบนจะไม่สามารถใช้ได้และไม่ได้มีการดัก command ที่ไม่มีอยู่จริงใน ftp
- ไม่ได้มีการ check timeout ในบางกรณี ทำให้อาจเกิด error ในการทดสอบโปรแกรม
- คำสั่ง get อาจมีบรรทัดเกินมาจากต้นฉบับ เช่น
ftp> get fkkaofk
200 PORT command successful.
550 This function is not supported on this system.

ftp>