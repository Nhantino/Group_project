# Hướng dẫn Push Code lên Parent Repo

## Phương án 1: Sử dụng Git Command Line

### Bước 1: Kiểm tra trạng thái hiện tại
```bash
# Kiểm tra các file đã thay đổi
git status

# Kiểm tra branch hiện tại (phải là main)
git branch
```

### Bước 2: Cập nhật code mới nhất từ remote
```bash
# Lấy code mới nhất từ parent repo về
git pull origin main
```

**Lưu ý:** Nếu có conflict, cần resolve conflict trước khi tiếp tục:
```bash
# Mở file có conflict, sửa và lưu lại
# Sau đó add file đã sửa
git add <tên-file-đã-sửa>
git commit -m "Resolve conflict"
```

### Bước 3: Thêm file vào staging area
```bash
# Thêm tất cả các file đã thay đổi
git add .

# Hoặc thêm từng file cụ thể
git add <tên-file-1> <tên-file-2>

# Hoặc thêm tất cả file của một loại
git add *.js
```

### Bước 4: Commit các thay đổi
```bash
# Commit với message rõ ràng
git commit -m "Mô tả ngắn gọn về thay đổi"

# Ví dụ commit message tốt:
git commit -m "Add user login feature"
git commit -m "Fix bug in product listing"
git commit -m "Update documentation for API endpoints"
```

**Quy tắc viết commit message:**
- Sử dụng động từ chỉ hành động: Add, Fix, Update, Remove, Refactor
- Ngắn gọn, rõ ràng (dưới 50 ký tự cho tiêu đề)
- Không kết thúc bằng dấu chấm
- Viết bằng tiếng Anh hoặc tiếng Việt có dấu

### Bước 5: Push code lên parent repo
```bash
# Push lên nhánh main
git push origin main

# Nếu gặp lỗi, có thể cần force push (CẨN THẬN!)
# Chỉ dùng khi chắc chắn
git push origin main --force
```

### Bước 6: Xác nhận đã push thành công
- Vào GitHub/GitLab kiểm tra code đã lên chưa
- Kiểm tra commit history
- Thông báo cho team biết đã push code

---

## Phương án 2: Sử dụng GitHub Desktop

### Bước 1: Mở GitHub Desktop
- Mở ứng dụng GitHub Desktop
- Chọn repository đang làm việc

### Bước 2: Kiểm tra các thay đổi
- Panel bên trái sẽ hiển thị các file đã thay đổi
- Tick chọn các file muốn commit
- Hoặc click "Select All" để chọn tất cả

![](https://docs.github.com/assets/images/help/desktop/commit-all.png)

### Bước 3: Fetch và Pull code mới nhất
- Click nút "Fetch origin" ở trên cùng
- Nếu có code mới, click "Pull origin" để cập nhật

**Xử lý conflict trong GitHub Desktop:**
- Nếu có conflict, GitHub Desktop sẽ báo
- Click "Open in [Editor]" để mở file conflict
- Sửa conflict và lưu lại
- Quay lại GitHub Desktop, file sẽ tự động được mark là resolved

### Bước 4: Commit các thay đổi
- Ở góc dưới bên trái, điền commit message:
  - **Summary:** Mô tả ngắn (bắt buộc)
  - **Description:** Mô tả chi tiết (tùy chọn)
- Click nút "Commit to main"

**Ví dụ commit message:**
```
Summary: Add user authentication
Description: 
- Implement login form
- Add JWT token handling
- Create protected routes
```

### Bước 5: Push code lên parent repo
- Sau khi commit, nút ở trên cùng sẽ đổi thành "Push origin"
- Click "Push origin" để đẩy code lên GitHub
- Chờ progress bar hoàn thành

### Bước 6: Xác nhận trên GitHub
- Click "View on GitHub" để mở repository trên web
- Kiểm tra commit đã lên chưa

---

## Quy trình làm việc hàng ngày

### Khi bắt đầu làm việc:
```bash
# 1. Pull code mới nhất về
git pull origin main

# 2. Bắt đầu code
# ...
```

### Trong khi làm việc:
```bash
# Commit thường xuyên (mỗi 30-60 phút hoặc sau mỗi tính năng nhỏ)
git add .
git commit -m "Descriptive message"
```

### Khi kết thúc ngày làm việc:
```bash
# 1. Commit tất cả thay đổi
git add .
git commit -m "End of day commit: summary of work"

# 2. Pull code mới (nếu có ai push trong ngày)
git pull origin main

# 3. Push lên remote
git push origin main
```

---

## Các lệnh Git hữu ích

### Kiểm tra thông tin
```bash
# Xem lịch sử commit
git log

# Xem lịch sử ngắn gọn
git log --oneline

# Xem chi tiết thay đổi
git diff

# Xem remote repository
git remote -v
```

### Hoàn tác thay đổi
```bash
# Hủy thay đổi chưa commit của một file
git checkout -- <tên-file>

# Hủy tất cả thay đổi chưa commit
git checkout -- .

# Hủy commit cuối cùng (giữ lại thay đổi)
git reset --soft HEAD~1

# Hủy commit cuối cùng (xóa luôn thay đổi)
git reset --hard HEAD~1
```

### Stash (Cất thay đổi tạm thời)
```bash
# Cất thay đổi
git stash

# Xem danh sách stash
git stash list

# Lấy lại thay đổi gần nhất
git stash pop

# Áp dụng stash cụ thể
git stash apply stash@{0}
```

---

## Xử lý các tình huống thường gặp

### Tình huống 1: Quên pull code trước khi push
```bash
# Git sẽ báo lỗi: "Updates were rejected"
# Giải pháp:
git pull origin main
# Resolve conflict nếu có
git push origin main
```

### Tình huống 2: Push nhầm code
```bash
# Nếu chưa ai pull code của bạn:
git reset --hard HEAD~1  # Quay lại commit trước
git push origin main --force  # Force push (CẨN THẬN!)

# Nếu đã có người pull:
git revert HEAD  # Tạo commit mới để hoàn tác
git push origin main
```

### Tình huống 3: Conflict khi pull
```bash
# Mở file conflict, tìm các dòng:
<<<<<<< HEAD
Thay đổi của bạn
=======
Thay đổi từ remote
>>>>>>> branch-name

# Sửa lại code theo ý muốn, xóa các dấu marker
# Sau đó:
git add <file-đã-sửa>
git commit -m "Resolve merge conflict"
git push origin main
```

---

## Checklist trước khi Push

- [ ] Đã pull code mới nhất về
- [ ] Code chạy không lỗi trên local
- [ ] Đã test các chức năng thay đổi
- [ ] Commit message rõ ràng, mô tả đúng thay đổi
- [ ] Không push file nhạy cảm (password, API key, .env)
- [ ] Đã resolve hết conflicts (nếu có)
- [ ] Thông báo cho team nếu có thay đổi quan trọng
