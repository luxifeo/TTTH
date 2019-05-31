# Hướng dẫn cài đặt IBM CPLEX và Python API

Yêu cầu: Cài đặt Python 3 64bit.

Tải tại [link](https://e5.onthehub.com/WebStore/OfferingDetails.aspx?o=4d1c8238-e141-e911-8113-000d3af41938&pmv=00000000-0000-0000-0000-000000000000&ws=9c9e538b-f243-e211-ad71-f04da23e67f6&vsro=8) chọn add to cart.

Đăng nhập bằng tài khoản 201*****@student.hust.edu.vn.

Tải về và cài đặt.

Tại thư mục cài đặt (mặc đinh Linux: /opt/ibm/ILOG/CPLEX***, Windows: C:\Program Files\IBM\ILOG\CPLEX***),
chạy lệnh sau:

Linux: sudo python3 python/setup.py install

Windows (run as administrator): python3 python\setup.py install

Chạy file solve.py với đầu vào là 1 file input và 1 file output

Cấu trúc file input:

Dòng 1: Đường đi pha 1

Các dòng tiếp theo: Mỗi dòng bao gồm Tọa độ X, Tọa độ Y, mức tiêu hao năng lượng, năng lượng còn lại hiện tại của 1 nút.

Cấu trúc file output:

Dòng 1: Thời gian sạc của các nút

Dòng 2: Các nút chết

Dòng 3: Tổng số nút chết


